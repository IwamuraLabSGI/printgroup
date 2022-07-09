//
//  imgproc.cpp
//  LLAH
//
//  Created by Katsuma Tanaka on 2015/06/15.
//  Copyright (c) 2015 Katsuma Tanaka. All rights reserved.
//

#include "imgproc.hpp"

#include "histogram.hpp"
#include "keypoint.hpp"

using namespace std;
using namespace llah;


#pragma mark - Feature Detection
//最小座標を求める
cv::Point minPoint(vector<cv::Point> contours){
  double minx = contours.at(0).x;
  double miny = contours.at(0).y;
  for(int i=1;i<contours.size(); i++){
    if(minx > contours.at(i).x){
      minx = contours.at(i).x;
    }
    if(miny > contours.at(i).y){
      miny = contours.at(i).y;
    }
  }
  return cv::Point(minx, miny);
}
//最大座標を求める
cv::Point maxPoint(vector<cv::Point> contours){
  double maxx = contours.at(0).x;
  double maxy = contours.at(0).y;
  for(int i=1;i<contours.size(); i++){
    if(maxx < contours.at(i).x){
      maxx = contours.at(i).x;
    }
    if(maxy < contours.at(i).y){
      maxy = contours.at(i).y;
    }
  }
  return cv::Point(maxx, maxy);
}
void llah::detectFeatures(const cv::Mat& image, vector<Keypoint>& keypoints, cv::Size kernelSize) {
    cv::Mat grayImage, binImage, invImage;
    
    // グレースケール変換
    // Convert to grayscale
    if (image.channels() == 1) {
        grayImage = image;
    } else {
        cv::cvtColor(image, grayImage, CV_BGR2GRAY);
    }
    
    // // 適応2値化
    // // Adaptive binarization
    // cv::adaptiveThreshold(grayImage, binImage, 255, cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY, 101, 10);
    
    // // ガウシアンフィルタによる平滑化
    // // Apply gaussian filter
    // cv::GaussianBlur(binImage, grayImage, kernelSize, 0, 0);
    
    // 2値化
    // Binarization
    cv::threshold(grayImage, binImage, 200, 255, cv::THRESH_BINARY);
    
    // ビット反転
    // Bitwise NOT
    // cv::bitwise_not(binImage, invImage);
    
	// taniguchi
	// invImage = grayImage;
    invImage = binImage;
    
    // 平滑化した画像の領域を取得する
    // Extract contours
    vector<vector<cv::Point>> contours;
    cv::findContours(invImage, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    cv::Scalar color( rand()&255, rand()&255, rand()&255 );
    //cv::drawContours(invImage, contours, -1, color, CV_FILLED, 8);
    //cv::imshow("out", invImage);
    //cv::waitKey(0);
    // 中心座標を得る
    // Get center points of contours
    keypoints.reserve(contours.size());
    unsigned int pointID = 0;
    
	// taniguchi
	cv::Mat im(image);
	// end

	for (auto ite=contours.begin(); ite!=contours.end(); ++ite) {
		if (contourArea(*ite, false) < 2) {
			ite = contours.erase(ite);
			--ite;
		}
	}
    double xmin;
    double xmax;
    double ymin;
    double ymax;
    for (unsigned int i = 0; i < contours.size(); i++) {
      
        cv::Moments moments = cv::moments(contours[i], false);
       
        double x = moments.m10 / moments.m00;
        double y = moments.m01 / moments.m00;
        //cout << contours[i] << endl;
        //double x = (xmin + xmax) /2;
        //double y = (ymin + ymax) /2; 
        
        if (!std::isnan(x) && !std::isnan(y)) { // Function isnan() is overloaded, so std:: is important
            keypoints.push_back(Keypoint(pointID++, x, y, cv::contourArea(contours[i])));
			// taniguchi
			 //cout << "[" << pointID << "] " << x << ", " << y << endl;
			cv::circle(im, cv::Point(x, y), 8, cv::Scalar(150, 0, 0), -1);
			// end
        }
    }
	  //taniguchi
	  //cout << endl;
	  //cv::imwrite("out.jpg", im);
	  //end
    //cv::imshow("out", im);
    //cv::waitKey(0);
}

void llah::detectAdaptiveFeatures(const cv::Mat& image, vector<Keypoint>& keypoints) {
    cv::Mat grayImage, binImage, invImage;
    
    // グレースケール変換
    // Convert to grayscale
    cv::cvtColor(image, grayImage, CV_BGR2GRAY);
    
    // 適応2値化
    // Adaptive binarization
    cv::adaptiveThreshold(grayImage, binImage, 255, cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY, 101, 10);
    
    // ビット反転
    // Bitwise NOT
    cv::bitwise_not(binImage, invImage);
    
    // 文字の輪郭抽出
    // Extract contours
    vector<vector<cv::Point>> contours;
    cv::findContours(invImage, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    
    // ヒストグラムの計算
    // Create a histogram
    Histogram hist(0, 1000, 1000);
    
    for (unsigned int i = 0; i < contours.size(); i++) {
        double area = cv::contourArea(contours.at(i));
        
        if (area > 2.0) {
            hist.addValue(area);
        }
    }
    
    // ガウシアンマスクサイズの推定
    // Estimate a gaussian mask size
    int kernelSize = hist.largestValue();
    kernelSize = kernelSize + (kernelSize + 1) % 2 + 2;
    
    // ガウシアンフィルタによる平滑化
    // Apply gaussian filter
    cv::GaussianBlur(binImage, grayImage, cv::Size(kernelSize, kernelSize), 0, 0);
    
    // 2値化
    // Binarization
    cv::threshold(grayImage, binImage, 200, 255, cv::THRESH_BINARY);
    
    // ビット反転
    // Bitwise NOT
    cv::bitwise_not(binImage, invImage);
    
    // 平滑化した画像の領域を取得する
    // Extract contours
    vector<vector<cv::Point>> blurredContours;
    cv::findContours(invImage, blurredContours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
    
    // 中心座標を得る
    // Get center points of contours
    unsigned int pointID = 0;
    
    for (unsigned int i = 0; i < blurredContours.size(); i++) {
        cv::Moments moments = cv::moments(blurredContours.at(i), false);
        int x = moments.m10 / moments.m00;
        int y = moments.m01 / moments.m00;
        int xx = x%10;
        x = x-xx;
        int yy = y%10;
        y = y-yy;
        cout << "x : "<<x <<"   y : " << y <<endl;
                if (!std::isnan(x) && !std::isnan(y)) {
            keypoints.push_back(Keypoint(pointID++, x, y, cv::contourArea(blurredContours.at(i))));
        }
    }
}


#pragma mark - Helpers

vector<cv::Rect> llah::dividedRects(const cv::Mat image, int rows, int cols) {
    vector<cv::Rect> rects(rows * cols);
    
    for (int row = 0; row < rows; row++) {
        for (int col = 0; col < cols; col++) {
            rects[row * cols + col] = cv::Rect((image.cols / cols) * col,
                                               (image.rows / rows) * row,
                                               image.cols / cols,
                                               image.rows / rows);
        }
    }
    
    return rects;
}
