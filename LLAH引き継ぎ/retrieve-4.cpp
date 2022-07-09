#include <iostream>
#include <string>
#include <vector>
#include <sstream> // stringstream
#include <iomanip> // setw, setfill
#include <chrono>

#include <opencv2/opencv.hpp>
#include <llah/llah.hpp>

using namespace std;
using std::ofstream;
 
void resize(cv::Mat& image, double maxWidth) {
    cv::Size size(image.cols, image.rows);

    if (size.width > maxWidth) {
        size.height = size.height * (maxWidth / size.width);
        size.width = maxWidth;

        cv::resize(image, image, size);
    }
}

cv::Mat split(string& input, char delimiter)
{
    istringstream stream(input);
    string field;
    cv::Mat result;
    while (getline(stream, field, delimiter)) {
        result.push_back(field);
    }
    return result;
}

//------------------------------------------------------------------------------------------------------------------------------------------------
//A-KAZEの関数
 

int AKAZE(int DB ,int QUERI , int COLOR, int TOTALDB ){
   const auto start = std::chrono::high_resolution_clock::now();
if(DB > 77000 || QUERI >77000 || DB == -1 || QUERI == -1){
    DB = 10;
}
   std::string a = std::to_string(DB);
   std::string b = std::to_string(QUERI);
   std::string c = "img_semi/";
   std::string d = ".jpg";
   std::string AKA = "AKA/";
   std::string e = c  + a + d;
   std::string f = c  + b + d; 
   std::string g = AKA  + a  + d; 
   int React = 0;
   if(DB != 50000){
    //比較用画像を読み込む (アルファチャンネル非対応のため、IMREAD_COLORで強制する)
    //cv::Mat scene1 = cv::imread(scene1_path , cv::IMREAD_COLOR);
    cv::Mat scene1 = cv::imread(e); 
    cv::Mat scene2 = cv::imread(f);
    
    //アルゴリズムにAKAZEを使用する
    auto algorithm = cv::AKAZE::create();

    // 特徴点抽出
    std::vector<cv::KeyPoint> keypoint1, keypoint2;
    algorithm->detect(scene1, keypoint1);
    algorithm->detect(scene2, keypoint2);

    // 特徴記述
    cv::Mat descriptor1, descriptor2;
    algorithm->compute(scene1, keypoint1, descriptor1);
    algorithm->compute(scene2, keypoint2, descriptor2);
    // マッチング (アルゴリズムにはBruteForceを使用)
    cv::Ptr<cv::DescriptorMatcher> matcher = cv::DescriptorMatcher::create("BruteForce");
    std::vector<cv::DMatch> match, match12, match21;
    matcher->match(descriptor1, descriptor2, match12);
    matcher->match(descriptor2, descriptor1, match21);
    int kaze;
    //クロスチェック(1→2と2→1の両方でマッチしたものだけを残して精度を高める)
    for (size_t i = 0; i < match12.size(); i++)
    {
      cv::DMatch forward = match12[i];
      cv::DMatch backward = match21[forward.trainIdx];
      if (backward.trainIdx == forward.queryIdx)
      {
        match.push_back(forward);
      }
      kaze = kaze + 1 ;
    }
    for (long unsigned int i = 0; i < match.size() - 1; i++) {
		double min = match[i].distance;

		int n = i;
		for (long unsigned int j = i + 1; j < match.size(); j++) {
			if (min > match[j].distance) {
				n = j;
				min = match[j].distance;
			}
		}
		std::swap(match[i], match[n]);
	}
    
	
    for(long unsigned int i = 0;i < match.size();i++){
        if(match[i].distance < 350){
            React = React + 1;
        }
    }
	match.erase(match.begin() + React, match.end());
   /*for (int i = 0; i < match.size() - 1; i++) {
        std::cout << match[i].distance << std::endl;
    }*/
    // マッチング結果の描画
    //cv::Mat dest;
    //cv::drawMatches(scene1, keypoint1, scene2, keypoint2, match, dest);
    //マッチング結果の書き出し
    //cv::imwrite(g, dest);
    //cv::imshow("output",dest);
    const auto end = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> elapsed = end - start;
    
    if(DB == (QUERI-1)%TOTALDB+1 && COLOR == 1){
    std::cout << "CYAN:::match(DB)::" << "\033[37;44m" << DB  <<  "\033[0m" << "  match(QUERI)::" << "\033[37;44m" << QUERI  <<  "\033[0m" << " output::" << "\033[37;44m" << React  <<  "\033[0m" <<  ", time: " << elapsed.count() << std::endl;
    }
    if(DB != (QUERI-1)%TOTALDB+1 && COLOR == 1){
    std::cout << "CYAN:::match(DB)::" << "\033[37;44m" << DB  <<  "\033[0m" << "  match(QUERI)::" << "\033[37;41m" << QUERI  <<  "\033[0m" << " output::" << "\033[37;44m" << React  <<  "\033[0m" <<  ", time: " << elapsed.count() << std::endl;
    }
    if(DB == (QUERI-1)%TOTALDB+1 && COLOR == 2){
    std::cout << "MAGENDA:::match(DB)::" << "\033[37;44m" << DB  <<  "\033[0m" << "  match(QUERI)::" << "\033[37;44m" << QUERI  <<  "\033[0m" << " output::" << "\033[37;41m" << React  <<  "\033[0m" <<  ", time: " << elapsed.count() << std::endl;
    }
    if(DB != (QUERI-1)%TOTALDB+1 && COLOR == 2){
    std::cout << "MAGENDA:::match(DB)::" << "\033[37;44m" << DB  <<  "\033[0m" << "  match(QUERI)::" << "\033[37;41m" << QUERI  <<  "\033[0m" << " output::" << "\033[37;41m" << React  <<  "\033[0m" <<  ", time: " << elapsed.count() << std::endl;
    }
    if(DB == (QUERI-1)%TOTALDB+1 && COLOR == 3){
    std::cout << "YELLOW:::match(DB)::" << "\033[37;44m" << DB  <<  "\033[0m" << "  match(QUERI)::" << "\033[37;44m" << QUERI  <<  "\033[0m" << " output::" << "\033[37;43m" << React  <<  "\033[0m" <<  ", time: " << elapsed.count() << std::endl;
    }
    if(DB != (QUERI-1)%TOTALDB+1 && COLOR == 3){
    std::cout << "YELLOW:::match(DB)::" << "\033[37;44m" << DB  <<  "\033[0m" << "  match(QUERI)::" << "\033[37;41m" << QUERI  <<  "\033[0m" << " output::" << "\033[37;43m" << React  <<  "\033[0m" <<  ", time: " << elapsed.count() << std::endl;
    }
   //-----------------------------------------------------------------------------------------------------------------------------------------
   }
   const auto notend = std::chrono::high_resolution_clock::now();
    const std::chrono::duration<double> notelapsed = notend - start;
   if(DB == 50000){
    std::cout << "Dub Nation : " << ", time: " << notelapsed.count() << std::endl;
   }
   return React;
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





int main(int argc, char *argv[]) {
    cout << "Loading database..." << endl;
    // Load database
    llah::Database dbCyan("documents.dbCyan");
    llah::Database dbMagenda("documents.dbMagenda");
    llah::Database dbYellow("documents.dbYellow");
        
    
    
        //枚数を変えた時変更する変数//////////////
        int Start = 5001;//処理のスタート
        int End = 7000;//処理のラスト
        int TOTALDB = 5000;//データベースの総枚数
        int DBStart = 1;//データベースのスタート
        int DBEnd = 5000;//データベースのラスト
        int SEIKIStart = 5001;//正規画像のスタート
        int SEIKIEnd = 10000;//正規画像のラスト
        int GIZOUStart = 10001;//偽造画像のスタート
        int GIZOUEnd = 15000;//偽造画像のラスト
        int AKAZEStart = 5001;
        int AKAZEEnd = 10000;
        int AKAZEsikiiti = 20;//AKAZEの閾値
        int TOTALSEIKI = 0;//いじらんくて良い奴(1)
            TOTALSEIKI = SEIKIEnd - SEIKIStart + 1;
        int TOTALGIZOU = 0;//いじらんくて良い奴(2)
            TOTALGIZOU = GIZOUEnd - GIZOUStart + 1;
        //int Jyoukenn = 0;//いじらんくて良い奴(3)
            //Jyoukenn = SEIKIStart - DBStart;
        //////////////////////////////////////////
        
        
        //結果集計の為の変数たち//////
        int  Cyanmatch1 = 0;
        int  Cyanmatch2 = 0;
        int  Cyanmiss1  = 0; 
        int  Cyanmiss2  = 0;
        int  Cyanmissmatch1 = 0;
        int  Cyanmissmatch2 = 0;
        int  Cyangizoumatch1 = 0;
        int  Cyangizoumiss1  = 0; 
        int  Cyangizoumissmatch1 = 0;
        int  Magendamatch1 = 0;
        int  Magendamatch2 = 0;
        int  Magendamiss1  = 0; 
        int  Magendamiss2  = 0;
        int  Magendamissmatch1 = 0;
        int  Magendamissmatch2 = 0;
        int  Magendagizoumatch1 = 0;
        int  Magendagizoumiss1  = 0; 
        int  Magendagizoumissmatch1 = 0;
        int  Yellowmatch1 = 0;
        int  Yellowmatch2 = 0;
        int  Yellowmiss1  = 0; 
        int  Yellowmiss2  = 0;
        int  Yellowmissmatch1 = 0;
        int  Yellowmissmatch2 = 0;
        int  Yellowgizoumatch1 = 0;
        int  Yellowgizoumiss1  = 0; 
        int  Yellowgizoumissmatch1 = 0;
        ////////////////////////////////

        //LLAH全体の変数たち///////////
        int CyanScoring[20000];
        int MagendaScoring[20000];
        int YellowScoring[20000];
        int ALLScoring[20000];
        int ALL = 0;
        int ALLS = 0;
        int CyanALL = 0;
        int CyanALLS = 0;
        int MagendaALL = 0;
        int MagendaALLS = 0;
        int YellowALL = 0;
        int YellowALLS = 0;
        int gizouti = 0 ;
        int gizoutiheikinn = 0;
         double TOTALTIME = 0;
        ////////////////////////////////
        
        
        //第2,3候補用の変数たち////////
        int Cyansecond = 0 ;
        int Cyanthird = 0;
        int Magendasecond = 0 ;
        int Magendathird = 0;
        int Yellowsecond = 0 ;
        int Yellowthird = 0;
        //////////////////////////////

        //AKAZE関連の変数たち///////////
        int firstCyanAKAZEID[20000];
        int secondCyanAKAZEID[20000];
        int thirdCyanAKAZEID[20000];
        int firstMagendaAKAZEID[20000];
        int secondMagendaAKAZEID[20000];
        int thirdMagendaAKAZEID[20000];
        int firstYellowAKAZEID[20000];
        int secondYellowAKAZEID[20000];
        int thirdYellowAKAZEID[20000] ;
        int OK = 0;
        int BATU = 0;
        int GIZOU = 0;
        int ZENBU = 0;
        double AKAZETIME = 0;
        ofstream ofs("330kaitenn.csv");
        ///////////////////////////////


        //今は使っていない変数たち///////////////
        //int  Cyanmatch3 = 0;
        //int  Cyanmiss3  = 0;
        //int  Cyanmissmatch3 = 0;
        //int  Cyangizoumatch2 = 0;
        //int  Cyangizoumatch3 = 0;
        //int  Cyangizoumiss2  = 0;
        //int  Cyangizoumiss3  = 0;
        //int  Cyangizoumissmatch2 = 0;
        //int  Cyangizoumissmatch3 = 0;
        //int  Magendamatch3 = 0;
        //int  Magendamiss3  = 0;      
        //int  Magendamissmatch3 = 0;       
        //int  Magendagizoumatch2 = 0;
        //int  Magendagizoumatch3 = 0;      
        //int  Magendagizoumiss2  = 0;
        //int  Magendagizoumiss3  = 0;      
        //int  Magendagizoumissmatch2 = 0;
        //int  Magendagizoumissmatch3 = 0;
        //int  Yellowmatch3 = 0;   
        //int  Yellowmiss3  = 0;    
        //int  Yellowmissmatch3 = 0;     
        //int  Yellowgizoumatch2 = 0;
        //int  Yellowgizoumatch3 = 0;
        //int  Yellowgizoumiss2  = 0;
        //int  Yellowgizoumiss3  = 0;
        //int  Yellowgizoumissmatch2 = 0;
        //int  Yellowgizoumissmatch3 = 0;
        //int Cyansikiiti = 0;
        //int Magendasikiiti = 0;
        //int Yellowsikiiti = 0;
        //int  ALLmatch1 = 0;
        //int  ALLmatch2 = 0;
        //int  ALLmatch3 = 0;
        //int  ALLmiss1  = 0; 
        //int  ALLmiss2  = 0;
        //int  ALLmiss3  = 0;
        //int  ALLmissmatch1 = 0;
        //int  ALLmissmatch2 = 0;
        //int  ALLmissmatch3 = 0;
        //int  ALLgizoumatch1 = 0;
        //int  ALLgizoumatch2 = 0;
        //int  ALLgizoumatch3 = 0;
        //int  ALLgizoumiss1  = 0; 
        //int  ALLgizoumiss2  = 0;
        //int  ALLgizoumiss3  = 0;
        //int  ALLgizoumissmatch1 = 0;
        //int  ALLgizoumissmatch2 = 0;
        //int  ALLgizoumissmatch3 = 0;
        //int ALLdocumentID[9000] ;
        ///////////////////////////////////////////




    cout << "" << endl;
    cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
    cout << "-----------LLAH-----------" << endl;
    cout << "" << endl;
 

   
    //CyanでのLLAH高速検索処理//////////////////////////////////////////////////////////////////////
    for (int i = Start; i <= End ; i++) {
    if(DBStart <= i  && i <= DBEnd){
        cout << "DB: Cyan SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALDB<<", total:" << (i) << ")" << flush;
        }
    if(SEIKIStart <= i  && i <= SEIKIEnd){
        cout << "Collation: Cyan SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALSEIKI<<", total:" << (i) << ")" << flush;
        }
    if(GIZOUStart <= i  && i <= GIZOUEnd){
        cout << "Fake: Cyan SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALGIZOU<<", total:" << (i) << ")" << flush;
        }    
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

        // Retrieval
        llah::DocumentID CyandocumentID = -1;
        unsigned int Cyanscore = 0;
        llah::DocumentID SecondCyandocumentID = -1;
        unsigned int SecondCyanscore = 0;
        llah::DocumentID ThirdCyandocumentID = -1;
        unsigned int ThirdCyanscore = 0;
        const auto start = chrono::high_resolution_clock::now();

        CyandocumentID = dbCyan.findDocument(keypoints, nullptr, &Cyanscore , 0);
        if(CyandocumentID > End){
            CyandocumentID = -1;
        }
        SecondCyandocumentID = dbCyan.findDocument(keypoints, nullptr, &SecondCyanscore , 1);
        if(SecondCyandocumentID > End || CyandocumentID == SecondCyandocumentID){
            SecondCyandocumentID = -1;
        }
        ThirdCyandocumentID = dbCyan.findDocument(keypoints, nullptr, &ThirdCyanscore , 2);
        if(ThirdCyandocumentID > End || CyandocumentID == ThirdCyandocumentID){
            ThirdCyandocumentID = -1;
        }
        const auto end = chrono::high_resolution_clock::now();
        const chrono::duration<double> elapsed = end - start;
        TOTALTIME = TOTALTIME + elapsed.count();
        CyanScoring[i] = Cyanscore;
        cout << " -> Firstid: ";
		if (CyandocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";
		} else {
			if (CyandocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << CyandocumentID;
				cout << "\033[0m";
			} else {
				cout << "\033[37;41m";
				cout << CyandocumentID;
				cout << "\033[0m";
			}
		}
        cout << " -> Secondid: ";
		if (SecondCyandocumentID == -1 ) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";
		} else {
			if (SecondCyandocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd ) {
				cout << "\033[37;44m";
				cout << SecondCyandocumentID;
				cout << "\033[0m";
			} else {
				cout << "\033[37;41m";
				cout << SecondCyandocumentID;
				cout << "\033[0m";    
			}
		}
        cout << " -> Thirdid: ";
		if (ThirdCyandocumentID == -1 ) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";
            
		} else {
			if (ThirdCyandocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << ThirdCyandocumentID;
				cout << "\033[0m";
			} else {
				cout << "\033[37;41m";
				cout << ThirdCyandocumentID;
				cout << "\033[0m";
			}
		}
		if(i<= DBEnd || i >= GIZOUStart ){
        cout << ", Firstscore: " << Cyanscore << ", Secondscore: " << SecondCyanscore  << ", Thirdscore: " << ThirdCyanscore << ", time: " << elapsed.count() << " sec" << endl;
        }else
        {
        cout << ", Firstscore: " << Cyanscore << "/" <<CyanScoring[i-TOTALDB]<< ", Secondscore: " << SecondCyanscore << "/" <<CyanScoring[i-TOTALDB]<< ", Thirdscore: " << ThirdCyanscore << "/" <<CyanScoring[i-TOTALDB]<< ", time: " << elapsed.count() << " sec" << endl;
        }
        if(i <= SEIKIStart){
	    CyanALL = CyanALL + CyanScoring[i];
        }
        if(SEIKIStart <= i && i <= SEIKIEnd){
        CyanALLS = CyanALLS + CyanScoring[i];
        }
           if (CyandocumentID == -1) {
            if(i <= DBEnd)
            Cyanmiss1 +=1;
            if(SEIKIStart <= i && i <= SEIKIEnd)
            Cyanmiss2 +=1;
            if(GIZOUStart <= i && i <= GIZOUEnd)
            Cyangizoumiss1 +=1;
            
        }
        if (CyandocumentID == (i-1)%TOTALDB+1 ) {
                if(i <= DBEnd)
                Cyanmatch1 +=1;
                if(SEIKIStart <= i && i <= SEIKIEnd)
                Cyanmatch2 +=1;
                if(GIZOUStart <= i && i <= GIZOUEnd)
                Cyangizoumatch1 +=1;
                
        }
        if (CyandocumentID != (i-1)%TOTALDB+1 && CyandocumentID != -1  ) {
                if(i <= DBEnd)
                Cyanmissmatch1 +=1;
                if(SEIKIStart <= i && i <= SEIKIEnd)
                Cyanmissmatch2 +=1;
                if(GIZOUStart <= i && i <= GIZOUEnd)
                Cyangizoumissmatch1 +=1;
                
            
        }
        if (SecondCyandocumentID == (i-1)%TOTALDB+1 && CyandocumentID != SecondCyandocumentID) {
            Cyansecond = Cyansecond + 1;
        }
        if (ThirdCyandocumentID == (i-1)%TOTALDB+1  && CyandocumentID != ThirdCyandocumentID ) {
            Cyanthird = Cyanthird + 1;
        }
        
        if(i >= 0){
        if(CyandocumentID < 50001  ){
            firstCyanAKAZEID[i] = CyandocumentID;
            
        }else{
            firstCyanAKAZEID[i] = 10;
        }
        
        if(SecondCyandocumentID < 50001 ){
            secondCyanAKAZEID[i] = SecondCyandocumentID;
        }else{
            secondCyanAKAZEID[i] = 10;
        }
        if(ThirdCyandocumentID < 500001 ){
            thirdCyanAKAZEID[i] = ThirdCyandocumentID;
        }else{
            thirdCyanAKAZEID[i] = 10;
        }
        }
        if(DBStart <= i  && i <= DBEnd){
        ofs <<i<<","<<"Cyan DB"<<","<<","<<Cyanscore<<","<<","<<elapsed.count()<<endl;
        }
        if(SEIKIStart <= i  && i <= SEIKIEnd){
        ofs <<i<<","<<"Cyan Collation"<<","<<","<<Cyanscore<<","<<","<<elapsed.count()<<endl;
        }
        if(GIZOUStart <= i  && i <= GIZOUEnd){
        ofs <<i<<","<<"Cyan Fake"<<","<<","<<Cyanscore<<","<<","<<elapsed.count()<<endl;
        }    
       
        
    }

    



    //MagendaでのLLAH高速検索処理//////////////////////////////////////////////////////////////////////
    for (int i = Start; i <= End ; i++) {
    if(DBStart <= i  && i <= DBEnd){
        cout << "DB: Magenda SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALDB<<", total:" << (i) << ")" << flush;
        }
    if(SEIKIStart <= i  && i <= SEIKIEnd){
        cout << "Collation: Magenda SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALSEIKI<<", total:" << (i) << ")" << flush;
        }
    if(GIZOUStart <= i  && i <= GIZOUEnd){
        cout << "Fake: Magenda SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALGIZOU<<", total:" << (i) << ")" << flush;
        }    

        // Build file path
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        string filePath = "./Magenda_semi/" + ss.str() + ".jpg";

        // Load image
        cv::Mat image = cv::imread(filePath);

        // Resize
        resize(image, 1000.0);

        // Extract keypoints
        vector<llah::Keypoint> keypoints;
        llah::detectFeatures(image, keypoints);

        // Retrieval
        llah::DocumentID MagendadocumentID = -1;
        unsigned int Magendascore = 0;
        llah::DocumentID SecondMagendadocumentID = -1;
        unsigned int SecondMagendascore = 0;
        llah::DocumentID ThirdMagendadocumentID = -1;
        unsigned int ThirdMagendascore = 0;
        const auto start = chrono::high_resolution_clock::now();

        MagendadocumentID = dbMagenda.findDocument(keypoints, nullptr, &Magendascore ,0);
        if(MagendadocumentID > End){
            MagendadocumentID = -1;
        }
        SecondMagendadocumentID = dbMagenda.findDocument(keypoints, nullptr, &SecondMagendascore ,1);
         if(SecondMagendadocumentID > End || MagendadocumentID == SecondMagendadocumentID){
            SecondMagendadocumentID = -1;
        }
        ThirdMagendadocumentID = dbMagenda.findDocument(keypoints, nullptr, &ThirdMagendascore ,2);
         if(ThirdMagendadocumentID > End || MagendadocumentID == ThirdMagendadocumentID){
            ThirdMagendadocumentID = -1;
        }
        const auto end = chrono::high_resolution_clock::now();
        const chrono::duration<double> elapsed = end - start;
        TOTALTIME = TOTALTIME + elapsed.count();

        MagendaScoring[i] = Magendascore;
        cout << " -> Firstid: ";
		if (MagendadocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";

		} else {
			if (MagendadocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << MagendadocumentID;
				cout << "\033[0m";
                
			} else {
				cout << "\033[37;41m";
				cout << MagendadocumentID;
				cout << "\033[0m";
                
			}
		}
        cout << " -> Secondid: ";
		if (SecondMagendadocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";

		} else {
			if (SecondMagendadocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << SecondMagendadocumentID;
				cout << "\033[0m";
                
			} else {
				cout << "\033[37;41m";
				cout << SecondMagendadocumentID;
				cout << "\033[0m";
                
			}
		}
        cout << " -> Thirdid: ";
		if (ThirdMagendadocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";

		} else {
			if (ThirdMagendadocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << ThirdMagendadocumentID;
				cout << "\033[0m";
                
			} else {
				cout << "\033[37;41m";
				cout << ThirdMagendadocumentID;
				cout << "\033[0m";
                
			}
		}
		if(i<= DBEnd || i >= GIZOUStart){
        cout << ", Firstscore: " << Magendascore << ", Secondscore: " << SecondMagendascore << ", Thirdscore: " << ThirdMagendascore << ", time: " << elapsed.count() << " sec" << endl;
        } else {
        cout << ", Firstscore: " << Magendascore << "/" <<MagendaScoring[i-TOTALDB]<< ", Secondscore: " << SecondMagendascore << "/" <<MagendaScoring[i-TOTALDB]<< ", Thirdscore: " << ThirdMagendascore << "/" <<MagendaScoring[i-TOTALDB]<< ", time: " << elapsed.count() << " sec" << endl;
        }
        if(i <= DBEnd){
	    MagendaALL = MagendaALL + MagendaScoring[i];
        }
        if(SEIKIStart <= i && i <= SEIKIEnd){
        MagendaALLS = MagendaALLS + MagendaScoring[i];
        }
    


       if (MagendadocumentID == -1) {
            if(i <= DBEnd && DBStart <= i)
            Magendamiss1 +=1;
            if(SEIKIStart <= i && i <= SEIKIEnd)
            Magendamiss2 +=1;
            if(GIZOUStart < i && i< GIZOUEnd)
            Magendagizoumiss1 +=1;
       }
        if (MagendadocumentID == (i-1)%TOTALDB+1  ) {
                if(i <= DBEnd)
                Magendamatch1 +=1;
                if(SEIKIStart <= i && i <= SEIKIEnd)
                Magendamatch2 +=1;
                if(GIZOUStart < i && i< GIZOUEnd)
                Magendagizoumatch1 +=1;
        }
        if (MagendadocumentID != (i-1)%TOTALDB+1 && MagendadocumentID != -1  ) {
                if(i <= DBEnd)
                Magendamissmatch1 +=1;
                if(SEIKIStart <= i && i <= SEIKIEnd)
                Magendamissmatch2 +=1;
                if(GIZOUStart < i && i< GIZOUEnd)
                Magendagizoumissmatch1 +=1;
        }

        if (SecondMagendadocumentID == (i-1)%TOTALDB+1  && MagendadocumentID != SecondMagendadocumentID) {
            Magendasecond = Magendasecond + 1;
        }
        if (ThirdMagendadocumentID == (i-1)%TOTALDB+1  && MagendadocumentID != ThirdMagendadocumentID) {
            Magendathird = Magendathird + 1;
        }
        if(i >= 0){
            if(MagendadocumentID < 50001 ){
                firstMagendaAKAZEID[i] = MagendadocumentID;
                
            }else{
                firstMagendaAKAZEID[i] = 10;
                 
            }
            if(SecondMagendadocumentID < 50001 ){
                secondMagendaAKAZEID[i] = SecondMagendadocumentID;

            }else{
                secondMagendaAKAZEID[i] = 10;
            }
            if(ThirdMagendadocumentID < 50001 ){
                thirdMagendaAKAZEID[i] = ThirdMagendadocumentID;
            }else{
                thirdMagendaAKAZEID[i] = 10;
            }
         }
        if(DBStart <= i  && i <= DBEnd){
        ofs <<i<<","<<"Magenda DB"<<","<<","<<Magendascore<<","<<","<<elapsed.count()<<endl;
        }
        if(SEIKIStart <= i  && i <= SEIKIEnd){
        ofs <<i<<","<<"Magenda Collation"<<","<<","<<Magendascore<<","<<","<<elapsed.count()<<endl;
        }
        if(GIZOUStart <= i  && i <= GIZOUEnd){
        ofs <<i<<","<<"Magenda Fake"<<","<<","<<Magendascore<<","<<","<<elapsed.count()<<endl;
        }    
    }
    
    





    
     //YellowでのLLAH高速検索処理//////////////////////////////////////////////////////////////////////
    for (int i = Start; i <= End ; i++) {
    if(DBStart <= i  && i <= DBEnd){
        cout << "DB: Yellow SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALDB<<", total:" << (i) << ")" << flush;
        }
    if(SEIKIStart <= i  && i <= SEIKIEnd){
        cout << "Collation: Yellow SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALSEIKI<<", total:" << (i) << ")" << flush;
        }
    if(GIZOUStart <= i  && i <= GIZOUEnd){
        cout << "Fake: Yellow SERCHING... (" << ((i-1)%TOTALDB+1) << "/"<< TOTALGIZOU<<", total:" << (i) << ")" << flush;
        }    
        
        // Build file path
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        string filePath = "./Yellow_semi/" + ss.str() + ".jpg";

        // Load image
        cv::Mat image = cv::imread(filePath);

        // Resize
        resize(image, 1000.0);
        
        // Extract keypoints
        vector<llah::Keypoint> keypoints;
        llah::detectFeatures(image, keypoints);

        // Retrieval
        llah::DocumentID YellowdocumentID = -1;
        unsigned int Yellowscore = 0;
        llah::DocumentID SecondYellowdocumentID = -1;
        unsigned int SecondYellowscore = 0;
        llah::DocumentID ThirdYellowdocumentID = -1;
        unsigned int ThirdYellowscore = 0;
        const auto start = chrono::high_resolution_clock::now();        
        YellowdocumentID = dbYellow.findDocument(keypoints, nullptr, &Yellowscore,0);
        if (YellowdocumentID > End){
            YellowdocumentID = -1;
        }
        SecondYellowdocumentID = dbYellow.findDocument(keypoints, nullptr, &SecondYellowscore,1);
        if (SecondYellowdocumentID > End || YellowdocumentID == SecondYellowdocumentID){
            SecondYellowdocumentID = -1;
        }
        ThirdYellowdocumentID = dbYellow.findDocument(keypoints, nullptr, &ThirdYellowscore,2);
        if (ThirdYellowdocumentID > End || YellowdocumentID == ThirdYellowdocumentID){
            ThirdYellowdocumentID = -1;
        }
        const auto end = chrono::high_resolution_clock::now();
        const chrono::duration<double> elapsed = end - start;
        TOTALTIME = TOTALTIME + elapsed.count();

        YellowScoring[i] = Yellowscore;
        cout << " -> Firstid: ";
		if (YellowdocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";

		} else {
			if (YellowdocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << YellowdocumentID;
				cout << "\033[0m";
                
			} else {
				cout << "\033[37;41m";
				cout << YellowdocumentID;
				cout << "\033[0m";
                
			}
		}

        cout << " -> Secondid: ";
		if (YellowdocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";

		} else {
			if (SecondYellowdocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << SecondYellowdocumentID;
				cout << "\033[0m";
                
			} else {
				cout << "\033[37;41m";
				cout << SecondYellowdocumentID;
				cout << "\033[0m";
                
			}
		}

        cout << " -> Thirdid: ";
		if (ThirdYellowdocumentID == -1) {
			cout << "\033[37;41m";
			cout << "XX";
			cout << "\033[0m";

		} else {
			if (ThirdYellowdocumentID == (i-1)%TOTALDB+1 && i <= SEIKIEnd) {
				cout << "\033[37;44m";
				cout << ThirdYellowdocumentID;
				cout << "\033[0m";
                
			} else {
				cout << "\033[37;41m";
				cout << ThirdYellowdocumentID;
				cout << "\033[0m";
                
			}
		}
		if(i<= DBEnd || i >= GIZOUStart){
        cout << ", Firstscore: " << Yellowscore<< ", Secondscore: " << SecondYellowscore<< ", Thirdscore: " << ThirdYellowscore << ", time: " << elapsed.count() << " sec" << endl;
        }else
        {
        cout << ", Firstscore: " << Yellowscore << "/" <<YellowScoring[i-TOTALDB]<< ", Secondscore: " << SecondYellowscore << "/" <<YellowScoring[i-TOTALDB]<< ", Thirdscore: " << ThirdYellowscore << "/" <<YellowScoring[i-TOTALDB]<< ", time: " << elapsed.count() << " sec" << endl;
        }
        if(i <= DBEnd){
	    YellowALL = YellowALL + YellowScoring[i];
        }
        if(SEIKIStart <= i && i <= SEIKIEnd){
        YellowALLS = YellowALLS + YellowScoring[i];
        }

        if (YellowdocumentID == -1){
            if(i <= DBEnd)
            Yellowmiss1 +=1;
            if(SEIKIStart <= i && i <= SEIKIEnd)
            Yellowmiss2 +=1;
            if(GIZOUStart <= i && i <= GIZOUEnd)
            Yellowgizoumiss1 +=1;

            
            
        }
        if (YellowdocumentID == (i-1)%TOTALDB+1) {
                if(i <= DBEnd)
                Yellowmatch1 +=1;
                if(SEIKIStart <= i && i <= SEIKIEnd){
                Yellowmatch2 +=1;
               
                }
                if(GIZOUStart <= i && i <= GIZOUEnd){
                Yellowgizoumatch1 +=1;
                }
            
                
        }
        if (YellowdocumentID != (i-1)%TOTALDB+1 && YellowdocumentID != -1) {
                if(i <= DBEnd)
                Yellowmissmatch1 +=1;
                if(SEIKIStart <= i && i <= SEIKIEnd)
                Yellowmissmatch2 +=1;
                if(GIZOUStart <= i && i <= GIZOUEnd)
                Yellowgizoumissmatch1 +=1;
                
            
        }
        if (SecondYellowdocumentID == (i-1)%TOTALDB+1 && YellowdocumentID != SecondYellowdocumentID) {
            Yellowsecond = Yellowsecond + 1;
        }
        if (ThirdYellowdocumentID == (i-1)%TOTALDB+1  && YellowdocumentID != ThirdYellowdocumentID) {
            Yellowthird = Yellowthird + 1;
        }
        if(i >= 0){
            if(YellowdocumentID < 50001 ){
                firstYellowAKAZEID[i] = YellowdocumentID;
                 
            }else{
                firstYellowAKAZEID[i] = 10;
            }
            if(SecondYellowdocumentID < 50001 ){
                secondYellowAKAZEID[i] = SecondYellowdocumentID;
            }else{
                secondYellowAKAZEID[i] = 10;
            }
            if(ThirdYellowdocumentID < 50001 ){
                thirdYellowAKAZEID[i] = ThirdYellowdocumentID;
            }else{
                thirdYellowAKAZEID[i] = 10;
            }
            }
            if(DBStart <= i  && i <= DBEnd){
        ofs <<i<<","<<"Yellow DB"<<","<<","<<Yellowscore<<","<<","<<elapsed.count()<<endl;
        }
        if(SEIKIStart <= i  && i <= SEIKIEnd){
        ofs <<i<<","<<"Yellow Collation"<<","<<","<<Yellowscore<<","<<","<<elapsed.count()<<endl;
        }
        if(GIZOUStart <= i  && i <= GIZOUEnd){
        ofs <<i<<","<<"Yellow Fake"<<","<<","<<Yellowscore<<","<<","<<elapsed.count()<<endl;
        }    
    }
    
cout << "" << endl;
cout << "" << endl;
cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
cout << "-----------LLAH-----------" << endl;
cout << "" << endl;
cout <<"Cyan Database ：" << "正判定 " << Cyanmatch1 <<"/" << TOTALDB << " 判定不能 " << Cyanmiss1 <<"/"<< TOTALDB <<  " 誤判定  "<< Cyanmissmatch1 << "/" << TOTALDB << endl; 
cout <<"Cyan Collation：" << "正判定 " << Cyanmatch2 <<"/" << TOTALSEIKI << " 判定不能 " << Cyanmiss2 <<"/"<< TOTALSEIKI <<  " 誤判定  "<< Cyanmissmatch2 << "/" << TOTALSEIKI << endl;
cout <<"Cyan Fake     ：" << "正判定 " << Cyangizoumatch1 <<"/" << TOTALGIZOU << " 判定不能 " << Cyangizoumiss1 <<"/"<< TOTALGIZOU <<  " 誤判定  "<< Cyangizoumissmatch1 << "/" << TOTALGIZOU << endl;
cout <<"Magenda Database ：" << "正判定 " << Magendamatch1 <<"/" << TOTALDB << " 判定不能 " << Magendamiss1 <<"/"<< TOTALDB <<  " 誤判定  "<< Magendamissmatch1 << "/" << TOTALDB << endl; 
cout <<"Magenda Collation：" << "正判定 " << Magendamatch2 <<"/" << TOTALSEIKI << " 判定不能 " << Magendamiss2 <<"/"<< TOTALSEIKI <<  " 誤判定  "<< Magendamissmatch2 << "/" << TOTALSEIKI << endl;
cout <<"Magenda Fake     ：" << "正判定 " << Magendagizoumatch1 <<"/" << TOTALGIZOU << " 判定不能 " << Magendagizoumiss1 <<"/"<< TOTALGIZOU <<  " 誤判定  "<< Magendagizoumissmatch1 << "/" << TOTALGIZOU << endl;
cout <<"Yellow Database ：" << "正判定 " << Yellowmatch1 <<"/" << TOTALDB << " 判定不能 " << Yellowmiss1 <<"/"<< TOTALDB <<  " 誤判定  "<< Yellowmissmatch1 << "/" << TOTALDB << endl; 
cout <<"Yellow Collation：" << "正判定 " << Yellowmatch2 <<"/" << TOTALSEIKI << " 判定不能 " << Yellowmiss2 <<"/"<< TOTALSEIKI <<  " 誤判定  "<< Yellowmissmatch2 << "/" << TOTALSEIKI << endl;
cout <<"Yellow Fake     ：" << "正判定 " << Yellowgizoumatch1 <<"/" << TOTALGIZOU << " 判定不能 " << Yellowgizoumiss1 <<"/"<< TOTALGIZOU <<  " 誤判定  "<< Yellowgizoumissmatch1 << "/" << TOTALGIZOU << endl;
cout << "" << endl;
cout << "Cyan：2候補での正判定 " << Cyansecond << "/" << TOTALSEIKI - Cyanmatch2  << "  Magenda：2候補での正判定 " << Magendasecond << "/" << TOTALSEIKI - Magendamatch2  << "  Yellow：2候補での正判定 " << Yellowsecond << "/" << TOTALSEIKI - Yellowmatch2 << endl;
cout << "Cyan：3候補での正判定" << Cyanthird << "/" << TOTALSEIKI - Cyanmatch2 -Cyansecond << "  Magenda：3候補での正判定" << Magendathird << "/" << TOTALSEIKI - Magendamatch2 - Magendasecond  << "  Yellow：3候補での正判定" << Yellowthird << "/" << TOTALSEIKI - Yellowmatch2 - Yellowsecond << endl;
cout << "Cyan：得票平均   ::" << CyanALLS/TOTALSEIKI << "/" << CyanALL/TOTALDB << endl;
cout << "Magenda：得票平均::" << MagendaALLS/TOTALSEIKI << "/" << MagendaALL/TOTALDB << endl;
cout << "Yellow ：得票平均::" << YellowALLS/TOTALSEIKI << "/" << YellowALL/TOTALDB << endl;
cout << "偽造データ最多得票::" << gizouti << endl;
cout << "偽造データ平均得票::" << gizoutiheikinn/1000 << endl;
cout << "平均処理時間::" << TOTALTIME/(3*(End - Start)) << "  sec"<< endl;
cout << "" << endl;

cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
cout << "" << endl;
cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
cout << "-----------A-KAZE-----------" << endl;
cout << "" << endl;
    


//A-KAZEでの真贋判定ステップ///////////////////////////////////////////////////////////////////
 for (int i = Start; i <= End; i++) {
 if(AKAZEStart <= i && i <= AKAZEEnd){
       
        int Judge[10];
        for (int t = 0 ; t < 10 ;t++){
            Judge[t] = 0;
        }
        const auto AKAZEstart = std::chrono::high_resolution_clock::now();
        ALLScoring[i] = CyanScoring[i] + MagendaScoring[i] + YellowScoring[i];
        if(i <= DBEnd){
	    ALL = ALL + ALLScoring[i];
        }
        if(SEIKIStart <= i && i <= SEIKIEnd){
        ALLS = ALLS + ALLScoring[i];
        }
        if(GIZOUStart <= i && i <= GIZOUEnd ){
            gizoutiheikinn = gizoutiheikinn + ALLScoring[i];
            if(ALLScoring[i] > gizouti){
                gizouti = ALLScoring[i];
            }
        }
        cout << "A-KAZE  JUDGING... (" << ((i-1)%TOTALDB+1) << "/"<< AKAZEEnd - AKAZEStart+1<<", total:" << (i) << ")" << flush;
        cout << " -> LLAH Serchid: ";
		
        if(i<= DBEnd || i >= GIZOUStart){
        cout /*<< ", ALL::score: " << ALLScoring[i] <<"  = " <<  CyanScoring[i] << " + " <<  MagendaScoring[i] << " + " <<  YellowScoring[i]  */<< endl;
        }else
        {
        cout /*<< ", ALL::score: " << ALLScoring[i] << "/" <<ALLScoring[i-1000] <<"  = " <<  CyanScoring[i] << " + " <<  MagendaScoring[i] << " + " <<  YellowScoring[i]  */<< endl;
        }
        int HIKISUU[25];
        HIKISUU[0] = firstCyanAKAZEID[i];
        HIKISUU[1] = firstMagendaAKAZEID[i];
        HIKISUU[2] = firstYellowAKAZEID[i];
        HIKISUU[3] = secondCyanAKAZEID[i];
        HIKISUU[4] = secondMagendaAKAZEID[i];
        HIKISUU[5] = secondYellowAKAZEID[i];
        HIKISUU[6] = thirdCyanAKAZEID[i];
        HIKISUU[7] = thirdMagendaAKAZEID[i];
        HIKISUU[8] = thirdYellowAKAZEID[i];
        HIKISUU[9] = 100000;
        HIKISUU[10] = 100000;
        HIKISUU[11] = 100000;
        HIKISUU[12] = 100000;
        HIKISUU[13] = 100000;
        HIKISUU[14] = 100000;
        HIKISUU[15] = 100000;
        HIKISUU[16] = 100000;
        HIKISUU[17] = 100000;
        HIKISUU[18] = 100000;
        HIKISUU[19] = 100000;
        HIKISUU[20] = 100000;
        HIKISUU[21] = 100000;
        HIKISUU[22] = 100000;
        HIKISUU[23] = 100000;
        for(int k = 0; k < 9; k++){
            if(HIKISUU[0] == HIKISUU[k+1] || HIKISUU[k] == -1 )
                HIKISUU[k+1] = 50000;
            if(HIKISUU[1] == HIKISUU[k+2] || HIKISUU[k] == -1 )
                HIKISUU[k+2] = 50000;
            if(HIKISUU[2] == HIKISUU[k+3] || HIKISUU[k] == -1 )
                HIKISUU[k+3] = 50000;
            if(HIKISUU[3] == HIKISUU[k+4] || HIKISUU[k] == -1 )
                HIKISUU[k+4] = 50000;
            if(HIKISUU[4] == HIKISUU[k+5] || HIKISUU[k] == -1 )
                HIKISUU[k+5] = 50000;
            if(HIKISUU[5] == HIKISUU[k+6] || HIKISUU[k] == -1 )
                HIKISUU[k+6] = 50000;
            if(HIKISUU[6] == HIKISUU[k+7] || HIKISUU[k] == -1 )
                HIKISUU[k+7] = 50000;
            if(HIKISUU[7] == HIKISUU[k+8] || HIKISUU[k] == -1 )
                HIKISUU[k+8] = 50000;
            if(HIKISUU[8] == HIKISUU[k+9] || HIKISUU[k] == -1 )
                HIKISUU[k+9] = 50000;
            
        }
        int stop = 0;
        cout << "First" << endl;
        Judge[0] = AKAZE(HIKISUU[0],i,1,TOTALDB);
        if(Judge[0] > 20 ){
            stop = 1;}
        if(stop != 1)
        cout<< HIKISUU[1]<<endl;
        Judge[1] = AKAZE(HIKISUU[1],i,2,TOTALDB);
        if(Judge[1] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[2] = AKAZE(HIKISUU[2],i,3,TOTALDB);
        cout << "Second" << endl;
        if(Judge[2] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[3] = AKAZE(HIKISUU[3],i,1,TOTALDB);
        if(Judge[3] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[4] = AKAZE(HIKISUU[4],i,2,TOTALDB);
        if(Judge[4] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[5] = AKAZE(HIKISUU[5],i,3,TOTALDB);
        cout << "Third" << endl;
        if(Judge[5] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[6] = AKAZE(HIKISUU[6],i,1,TOTALDB);
        if(Judge[6] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[7] = AKAZE(HIKISUU[7],i,2,TOTALDB);
        if(Judge[7] > 20 ){
            stop = 1;}
        if(stop != 1)
        Judge[8] = AKAZE(HIKISUU[8],i,3,TOTALDB);
        
        //ituka gyouretude jikanntannsyuku
        int JudgeScore = 0;
        int JJ = 0;
        int JudgeDocument = -1;
        const auto AKAZEend = chrono::high_resolution_clock::now();
        const chrono::duration<double> AKAZEelapsed = AKAZEend - AKAZEstart;
        AKAZETIME = AKAZETIME + AKAZEelapsed.count();
        
        //Judge
        for(int j=0; j < 9; j++){
            if(Judge[j] > JudgeScore){
                JudgeScore = Judge[j];
                JJ = j;
            }
        }

        if(JudgeScore >= 0){
            if(JJ == 0){
                JudgeDocument = firstCyanAKAZEID[i];
            }
            if(JJ == 1){
                JudgeDocument = firstMagendaAKAZEID[i];
            }
            if(JJ == 2){
                JudgeDocument = firstYellowAKAZEID[i];
            }
            if(JJ == 3){
                JudgeDocument = secondCyanAKAZEID[i];
            }
            if(JJ == 4){
                JudgeDocument = secondMagendaAKAZEID[i];
            }
            if(JJ == 5){
                JudgeDocument = secondYellowAKAZEID[i];
            }
            if(JJ == 6){
                JudgeDocument = thirdCyanAKAZEID[i];
            }
            if(JJ == 7){
                JudgeDocument = thirdMagendaAKAZEID[i];
            }
            if(JJ == 8){
                JudgeDocument = thirdYellowAKAZEID[i];
            }
        }

       cout << "" << endl;
        if(JudgeDocument == (i-1)%TOTALDB +1 && JudgeScore >  AKAZEsikiiti){
        cout << "JUDGE ID::" << "\033[37;44m" << JudgeDocument  <<  "\033[0m" << "  JUDGESCORE::" <<  JudgeScore  << endl;
        OK = OK + 1;
        }else{
        if(JudgeDocument != (i-1)%TOTALDB +1 && JudgeScore >  AKAZEsikiiti){
        cout << "JUDGE ID::" << "\033[37;41m" << JudgeDocument  <<  "\033[0m" << "  JUDGESCORE::" <<  JudgeScore  << endl;
        BATU = BATU + 1;
        ofs <<i<<","<<"MISS MATCH"<<","<<","<<JudgeDocument<<endl;
        }else{
        cout << "JUDGE ID::" << "\033[37;41m" << "XXXXX"  <<  "\033[0m" << endl;  
        GIZOU = GIZOU + 1;  
        ofs <<i<<","<<"NO MATCH"<<","<<","<<JudgeDocument<<endl;
        }
        }
        cout << "" << endl;
        ZENBU = OK + BATU + GIZOU;
        if(DBStart <= i  && i <= DBEnd){
        ofs <<i<<","<<"A-KAZE DB"<<","<<JudgeScore<<","<<","<<","<<AKAZEelapsed.count()<<endl;
        }
        if(SEIKIStart <= i  && i <= SEIKIEnd){
        ofs <<i<<","<<"A-KAZE Collation"<<","<<JudgeScore<<","<<","<<","<<AKAZEelapsed.count()<<endl;
        }
        if(GIZOUStart <= i  && i <= GIZOUEnd){
        ofs <<i<<","<<"A-KAZE Fake"<<","<<JudgeScore<<","<<","<<","<<AKAZEelapsed.count()<<endl;
        }    
       
        }
    }
        


cout << "" << endl;
cout << "" << endl;
cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
cout << "-----------LLAH-----------" << endl;
cout << "" << endl;
cout <<"Cyan Database ：" << "正判定 " << Cyanmatch1 <<"/" << TOTALDB << " 判定不能 " << Cyanmiss1 <<"/"<< TOTALDB <<  " 誤判定  "<< Cyanmissmatch1 << "/" << TOTALDB << endl; 
cout <<"Cyan Collation：" << "正判定 " << Cyanmatch2 <<"/" << TOTALSEIKI << " 判定不能 " << Cyanmiss2 <<"/"<< TOTALSEIKI <<  " 誤判定  "<< Cyanmissmatch2 << "/" << TOTALSEIKI << endl;
cout <<"Cyan Fake     ：" << "正判定 " << Cyangizoumatch1 <<"/" << TOTALGIZOU << " 判定不能 " << Cyangizoumiss1 <<"/"<< TOTALGIZOU <<  " 誤判定  "<< Cyangizoumissmatch1 << "/" << TOTALGIZOU << endl;
cout <<"Magenda Database ：" << "正判定 " << Magendamatch1 <<"/" << TOTALDB << " 判定不能 " << Magendamiss1 <<"/"<< TOTALDB <<  " 誤判定  "<< Magendamissmatch1 << "/" << TOTALDB << endl; 
cout <<"Magenda Collation：" << "正判定 " << Magendamatch2 <<"/" << TOTALSEIKI << " 判定不能 " << Magendamiss2 <<"/"<< TOTALSEIKI <<  " 誤判定  "<< Magendamissmatch2 << "/" << TOTALSEIKI << endl;
cout <<"Magenda Fake     ：" << "正判定 " << Magendagizoumatch1 <<"/" << TOTALGIZOU << " 判定不能 " << Magendagizoumiss1 <<"/"<< TOTALGIZOU <<  " 誤判定  "<< Magendagizoumissmatch1 << "/" << TOTALGIZOU << endl;
cout <<"Yellow Database ：" << "正判定 " << Yellowmatch1 <<"/" << TOTALDB << " 判定不能 " << Yellowmiss1 <<"/"<< TOTALDB <<  " 誤判定  "<< Yellowmissmatch1 << "/" << TOTALDB << endl; 
cout <<"Yellow Collation：" << "正判定 " << Yellowmatch2 <<"/" << TOTALSEIKI << " 判定不能 " << Yellowmiss2 <<"/"<< TOTALSEIKI <<  " 誤判定  "<< Yellowmissmatch2 << "/" << TOTALSEIKI << endl;
cout <<"Yellow Fake     ：" << "正判定 " << Yellowgizoumatch1 <<"/" << TOTALGIZOU << " 判定不能 " << Yellowgizoumiss1 <<"/"<< TOTALGIZOU <<  " 誤判定  "<< Yellowgizoumissmatch1 << "/" << TOTALGIZOU << endl;
cout << "" << endl;
cout << "Cyan：2候補での正判定 " << Cyansecond << "/" << TOTALSEIKI - Cyanmatch2  << "  Magenda：2候補での正判定 " << Magendasecond << "/" << TOTALSEIKI - Magendamatch2  << "  Yellow：2候補での正判定 " << Yellowsecond << "/" << TOTALSEIKI - Yellowmatch2 << endl;
cout << "Cyan：3候補での正判定" << Cyanthird << "/" << TOTALSEIKI - Cyanmatch2 -Cyansecond << "  Magenda：3候補での正判定" << Magendathird << "/" << TOTALSEIKI - Magendamatch2 - Magendasecond  << "  Yellow：3候補での正判定" << Yellowthird << "/" << TOTALSEIKI - Yellowmatch2 - Yellowsecond << endl;
cout << "Cyan：得票平均   ::" << CyanALLS/TOTALSEIKI << "/" << CyanALL/TOTALDB << endl;
cout << "Magenda：得票平均::" << MagendaALLS/TOTALSEIKI << "/" << MagendaALL/TOTALDB << endl;
cout << "Yellow ：得票平均::" << YellowALLS/TOTALSEIKI << "/" << YellowALL/TOTALDB << endl;
cout << "偽造データ最多得票::" << gizouti << endl;
cout << "偽造データ平均得票::" << gizoutiheikinn/1000 << endl;
cout << "平均処理時間::" << TOTALTIME/(3*(End - Start)) << "  sec"<< endl;
cout << "" << endl;


cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------" << endl;
cout << "-----------A-KAZE-----------" << endl;
cout << "" << endl;
cout << "正判定::::" << OK  << " / " <<  ZENBU << endl;
cout << "誤判定::::" << BATU  << " / " <<  ZENBU << endl;
cout << "判定不能::" << GIZOU  << " / " <<  ZENBU << endl;
cout << "A-KAZEtime: " << AKAZETIME/(End-Start) << " sec" << endl;
cout << "" << endl;
return 0;
}
