#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

int main(int argc, char** argv)
{
    // Görüntü yükleme ve boyutlandırma
    Mat img = imread("path/to/image.jpg");
    resize(img, img, Size(500, 500));

    // Görüntüyü gri tona dönüştürme
    Mat gray;
    cvtColor(img, gray, COLOR_BGR2GRAY);

    // Gövde bölgesinin tespiti için threshold uygulama
    int threshold_value = 200;
    Mat binary;
    threshold(gray, binary, threshold_value, 255, THRESH_BINARY_INV);

    // Gövde bölgesini tespit etmek için yatay çizgi hesaplama
    int height = binary.rows;
    int width = binary.cols;
    int line_position = int(height * 0.6);
    Mat line_pixels = binary.row(line_position);
    int line_pixels_sum = countNonZero(line_pixels);

    // Gövde bölgesinin hesaplanması
    Mat torso_pixels = binary(Rect(0, line_position, width, height - line_position));
    int torso_pixels_sum = countNonZero(torso_pixels);
    float torso_pixels_ratio = float(torso_pixels_sum) / float(width * (height - line_position));

    // Gövde bölgesinin tespit edilmesi
    if (line_pixels_sum > (width / 3) && torso_pixels_ratio > 0.05) {
        line(img, Point(0, line_position), Point(width, line_position), Scalar(0, 255, 0), 2);
        imshow("Image with torso detection", img);
    }
    else {
        std::cout << "Torso not found." << std::endl;
    }

    waitKey(0);
    return 0;
}
