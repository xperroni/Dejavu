/*
Copyright (c) Helio Perroni Filho <xperroni@gmail.com>

This file is part of Dejavu.

Dejavu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Dejavu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Dejavu. If not, see <http://www.gnu.org/licenses/>.
*/

#include <clarus/core/list.hpp>
using clarus::List;

#include <clarus/io/viewer.hpp>

#include <clarus/vision/depths.hpp>
#include <clarus/vision/images.hpp>

#include <cight/drift_estimator.hpp>
using cight::Estimator;

#include <cight/drift_reduce.hpp>
using cight::reduce_slip;

#include <cight/feature_selector.hpp>
using cight::Selector;

#include <cight/video_stream.hpp>
using cight::SensorStream;
using cight::VideoStream;

#include <cight/visual_matcher.hpp>
using cight::StreamMatcher;
using cight::VisualMatcher;

#include <boost/bind.hpp>

#include <iostream>
#include <fstream>
#include <string>

void test_interpolator(const std::string &path) {
    cv::Mat similarities = depths::load(path);
    cv::Point3f line = cight::interpolateHough(similarities);
    const cv::Point a = cight::lineP0(line);
    const cv::Point b = cight::linePn(line, similarities.size());

    std::cerr << a << ", " << b << std::endl;

    cv::Mat bgr = depths::bgr(similarities);
    cv::line(bgr, a, b, cv::Scalar(0, 0, 0));
    viewer::show("Similarities", images::scale(bgr, cv::Size(300, 300)));
    cv::waitKey();
}

void dejavu_run(const std::string &teachPath, const std::string &replayPath) {
    VideoStream teachStream(teachPath, 10);
    VideoStream replayStream(replayPath, 10);
/*
    cv::GoodFeaturesToTrackDetector detector(20, 0.01, 30);
    Selector cornerSelector = boost::bind(cight::selectGoodFeatures, boost::ref(detector), _1, _2);
    Selector selector = boost::bind(cight::selectBorders, cornerSelector, 0.5, _1, _2);

    cv::GoodFeaturesToTrackDetector detector(10, 0.01, 30);
    Selector selector = boost::bind(cight::selectGoodFeatures, boost::ref(detector), _1, _2);
*/

    cv::FastFeatureDetector detector(20);
    Selector fastSelector = boost::bind(cight::selectFAST, boost::ref(detector), _1, _2);
    Selector disjointSelector = boost::bind(cight::selectDisjoint, fastSelector, _1, _2);
    Selector selector = boost::bind(cight::selectAtMost, disjointSelector, 10, _1, _2);

    VisualMatcher matcher(
        teachStream, replayStream, cv::Size(10, 25),
        selector, 30, 80,
        cight::interpolateSlide
    );

    matcher.computeMatching();

    Estimator estimator(50, 5, 2, matcher);
    std::ofstream file("drift.txt");
    reduce_slip drift;
    for (;;) {
        cv::Mat responses = estimator();
        if (responses.empty()) {
            break;
        }

        file << responses << std::endl;
        std::cerr << drift(responses) << std::endl;
    }
}

int dejavu_run(int argc, char *argv[]) {
//    dejavu_run(argv[1], argv[2]);
    dejavu_run(
        "/home/helio/Roboken/Data/Straight/2014-12-16-yaw-01-00/video.mpg",
        "/home/helio/Roboken/Data/Straight/2014-12-16-yaw-03-00/video.mpg"
    );
}

int main(int argc, char *argv[]) {
    return dejavu_run(argc, argv);
}
