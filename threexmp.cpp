#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

struct Packet {
  int length;
  int width;
  int height;
};

std::condition_variable cond_var;
std::mutex m;

std::queue<Packet> packet_queue;

void parcel_delivery() {
  int counter = 0;
  while (true) {
    // Perform some long running task
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::cout << "Work is done and data is ready!" << std::endl;
    Packet new_packet{counter, counter + 1, counter + 2};
    counter = counter +1;
    {
      // 3: Lock the mutex before writing to the queue and notify the waiting
      // thread
      std::lock_guard<std::mutex> l{m};
      packet_queue.push(new_packet);
    }
    cond_var.notify_one();
  }
}

void recipient1() {
  while (true) {
    // 2: Use a unique_lock and check the condition with a predicate
    std::unique_lock<std::mutex> lock{m};
    cond_var.wait(lock, []() { return !packet_queue.empty(); });
    
    auto new_packet = packet_queue.front();
    packet_queue.pop();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    lock.unlock();
    std::cout << "Received new packet with dimension: " << new_packet.length
              << "; " << new_packet.width << "; " << new_packet.height
              << std::endl;
  }
}

void recipient2() {
  while (true) {
    // 2: Use a unique_lock and check the condition with a predicate
    std::unique_lock<std::mutex> lock{m};
    cond_var.wait(lock, []() { return !packet_queue.empty(); });
    
    auto new_packet = packet_queue.front();
    packet_queue.pop();
    std::this_thread::sleep_for(std::chrono::seconds(2));
    lock.unlock();
    std::cout << "Received new packet with dimension: " << new_packet.length
              << "; " << new_packet.width << "; " << new_packet.height
              << std::endl;
  }
}

int main(int argc, const char **argv) {
  // 1: Start two threads: Producer and consumer
  std::thread producing_thread(parcel_delivery);
  std::thread consuming_thread(recipient1);
  std::thread consuming_thread2(recipient1);
  producing_thread.join();
  consuming_thread.join();
  consuming_thread2.join();
  return 0;
}
