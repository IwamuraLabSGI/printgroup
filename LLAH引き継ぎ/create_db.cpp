#include <iostream>
#include <string>
#include <vector>
#include <sstream> // stringstream
#include <iomanip> // setw, setfill

#include <opencv2/opencv.hpp>
#include <llah/llah.hpp>

using namespace std;


static void resize(cv::Mat& image, double maxWidth) {
    cv::Size size(image.cols, image.rows);

    if (size.width > maxWidth) {
        size.height = size.height * (maxWidth / size.width);
        size.width = maxWidth;

        cv::resize(image, image, size);
    }
}

int main(int argc, char *argv[]) {
    cout << "Building database..." << endl;
    // Create database
    
    llah::Database dbCyan((256)*5 + 27, 7, 6, 4);
    llah::Database dbMagenda((256)*5 + 27, 7, 6, 4);
    llah::Database dbYellow((256)*5 + 27, 7, 6, 4);
    //db.load("documents.db");
    dbCyan.setRemoveRedundancy(false);
    dbCyan.setSampleKeypoints(false);
    dbCyan.setNumberOfKeypointsToSample(200);
    dbCyan.setSampleFeatures(false);
    dbCyan.setNumberOfFeaturesToSample(4000000000);
    dbCyan.setListLengthLimit(50000000000);

    dbMagenda.setRemoveRedundancy(false);
    dbMagenda.setSampleKeypoints(false);
    dbMagenda.setNumberOfKeypointsToSample(2000);
    dbMagenda.setSampleFeatures(false);
    dbMagenda.setNumberOfFeaturesToSample(4000000000);
    dbMagenda.setListLengthLimit(5000);

    dbYellow.setRemoveRedundancy(false);
    dbYellow.setSampleKeypoints(false);
    dbYellow.setNumberOfKeypointsToSample(200);
    dbYellow.setSampleFeatures(false);
    dbYellow.setNumberOfFeaturesToSample(4000000000);
    dbYellow.setListLengthLimit(50000000000);
    int Start = 1;
    int End = 1000;
    //dbCyan.load("documents.dbCyan");
    //dbMagenda.load("documents.dbMagenda");
    //dbYellow.load("documents.dbYellow");
    for (int i = Start; i <= End ; i++) {
        cout << "Cyan  Processing... (" << (i) << "/"<<End <<")"<< flush;

        // Build file path
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        string filePath = "./Cyan_semi/" + ss.str() + ".jpg";

        // Load image
        cv::Mat image = cv::imread(filePath);

        // Resize
        resize(image, 1000.0);

        // Extract keypoints
        vector<llah::Keypoint> keypoints;
        llah::detectFeatures(image, keypoints);
        
        // Add to database
        vector<cv::Rect> rects = llah::dividedRects(image, 4, 2);
        dbCyan.addDocument(keypoints, i, &rects);
        //KJ = db.removeRedundancy() ;
        //cout << "hash: " << KJ << endl;
        cout << " -> id: " << i << ", keypoints: " << keypoints.size() << endl;
        //imshow("output",image);
        //cv::waitKey(0);
        


        cout << "Magenda Processing... (" << (i) << "/"<<End <<")" << flush;

        // Build file path
        stringstream Magendass;
        Magendass << setw(2) << setfill('0') << i;
        string MagendafilePath = "./Magenda_semi/" + Magendass.str() + ".jpg";

        // Load image
        cv::Mat Magendaimage = cv::imread(MagendafilePath);

        // Resize
        resize(Magendaimage, 1000.0);

        // Extract keypoints
        vector<llah::Keypoint> Magendakeypoints;
        llah::detectFeatures(Magendaimage, Magendakeypoints);
        
        // Add to database
        vector<cv::Rect> Magendarects = llah::dividedRects(Magendaimage, 4, 2);
        dbMagenda.addDocument(Magendakeypoints, i, &Magendarects);
        //KJ = db.removeRedundancy() ;
        //cout << "hash: " << KJ << endl;
        cout << " -> id: " << i << ", keypoints: " << Magendakeypoints.size() << endl;
        //imshow("output",image);
        //cv::waitKey(0);
      



        cout << "Yellow Processing... (" << (i) << "/"<<End <<")" << flush;

        // Build file path
        stringstream Yellowss;
        Yellowss << setw(2) << setfill('0') << i;
        string YellowfilePath = "./Yellow_semi/" + Yellowss.str() + ".jpg";

        // Load image
        cv::Mat Yellowimage = cv::imread(YellowfilePath);

        // Resize
        resize(Yellowimage, 1000.0);

        // Extract keypoints
        vector<llah::Keypoint> Yellowkeypoints;
        llah::detectFeatures(Yellowimage, Yellowkeypoints);
        
        // Add to database
        vector<cv::Rect> Yellowrects = llah::dividedRects(Yellowimage, 4, 2);
        dbYellow.addDocument(Yellowkeypoints, i, &Yellowrects);
        //KJ = db.removeRedundancy() ;
        //cout << "hash: " << KJ << endl;
        cout << " -> id: " << i << ", keypoints: " << Yellowkeypoints.size() << endl;
        //imshow("output",image);
        //cv::waitKey(0);
       

    
    

    }
    
	// cout << "Processing... (" << (1) << "/1)" << flush;
	// string filePath = "./testimages/01.jpg";
	// cv::Mat image = cv::imread(filePath);
	// resize(image, 1000.0);
	// vector<llah::Keypoint> keypoints;
	// llah::detectFeatures(image, keypoints);
	// vector<cv::Rect> rects = llah::dividedRects(image, 4, 2);
	// db.addDocument(keypoints, 1, &rects);
	// cout << " -> id: " << 1 << ", keypoints: " << keypoints.size() << endl;


    
// Write to file
    
    dbCyan.save("documents.dbCyan");
    dbMagenda.save("documents.dbMagenda");
    dbYellow.save("documents.dbYellow");
    cout << " done." << endl;


    return 0;
}
