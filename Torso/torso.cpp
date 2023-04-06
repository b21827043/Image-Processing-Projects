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

    // Görüntüdeki kenarları belirleme
    Mat edges;
    Canny(gray, edges, 100, 200);

    // Kenarları genişletme
    Mat kernel = getStructuringElement(MORPH_RECT, Size(5, 5));
    Mat dilated_edges;
    dilate(edges, dilated_edges, kernel, Point(-1,-1), 1);

    // Kenarların dış hatlarını bulma
    std::vector<std::vector<Point>> contours;
    std::vector<Vec4i> hierarchy;
    findContours(dilated_edges, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

    // Görüntüdeki en büyük kontur bulma
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
    RotatedRect rect = minAreaRect(max_contour);
    Point2f box_points[4];
    rect.points(box_points);

    // Dikdörtgen kutuyu çizme
    for (int i = 0; i < 4; i++)
    {
        line(img, box_points[i], box_points[(i+1)%4], Scalar(0, 255, 0), 2);
    }

    // Görüntüyü gösterme
    imshow("Image", img);
    waitKey(0);
    destroyAllWindows();

    return 0;
}
