#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

int main()
{
    // Görüntüyü yükleme
    Mat img = imread("path/to/image.jpg");

    // Görüntüyü boyutlandırma ve gri tonlamaya dönüştürme
    resize(img, img, Size(500, 500));
    Mat gray;
    cvtColor(img, gray, COLOR_BGR2GRAY);

    // Görüntüyü eşikleme
    Mat binary;
    threshold(gray, binary, 127, 255, THRESH_BINARY);

    // Morfolojik işlemler
    Mat kernel = getStructuringElement(MORPH_RECT, Size(15, 15));
    morphologyEx(binary, binary, MORPH_CLOSE, kernel);

    // Konturları bulma
    std::vector<std::vector<Point>> contours;
    std::vector<Vec4i> hierarchy;
    findContours(binary, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

    // En büyük konturu bulma
    int max_contour_index = -1;
    double max_contour_area = 0.0;
    for (int i = 0; i < contours.size(); i++)
    {
        double area = contourArea(contours[i]);
        if (area > max_contour_area)
        {
            max_contour_area = area;
            max_contour_index = i;
        }
    }
    std::vector<Point> max_contour = contours[max_contour_index];

    // Konturun minimum dikdörtgen kutusunu bulma
    Rect bounding_rect = boundingRect(max_contour);

    // Dikdörtgen kutuyu çizme
    rectangle(img, bounding_rect, Scalar(0, 255, 0), 2);

    // Görüntüyü gösterme
    imshow("Image", img);
    waitKey(0);
    destroyAllWindows();

    return 0;
}
