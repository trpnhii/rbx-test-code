# Tìm Đường Trong Đồ Thị Lớn

## 📌 Mô tả bài toán

Bạn được cung cấp một **đồ thị vô hướng có trọng số** và yêu cầu xây dựng một hệ thống hỗ trợ:

1. **Tìm đường đi ngắn nhất** giữa hai đỉnh bất kỳ.
2. **Hỗ trợ tìm kiếm trong thời gian thực** – kết quả trả về nhanh dù số lượng dữ liệu lớn.
3. **Cập nhật động dữ liệu đồ thị** – thêm đỉnh hoặc cạnh mới bất kỳ lúc nào.
4. **Tối ưu giải thuật** để đảm bảo hệ thống vận hành tốt trong quy mô rất lớn.

## 🌍 Ứng dụng thực tế

Bài toán này có nhiều ứng dụng thực tế như:

- **Hệ thống chỉ đường giao thông** (Google Maps, Grab).
- **Mạng máy tính** – tìm đường đi ngắn nhất giữa các máy chủ hoặc router.
- **Phân tích mạng xã hội** – xác định mức độ kết nối giữa người dùng.
- **Gợi ý sản phẩm** – đồ thị kết nối giữa người dùng và mặt hàng.
- **Tối ưu crawling và phân tích đồ thị web**.

---

## 🧠 Mô hình hóa bài toán

### Input

- Dòng đầu: `n m s t` – số đỉnh, số cạnh, đỉnh bắt đầu, đỉnh kết thúc.
- `m` dòng tiếp theo: mỗi dòng `u v w` – cạnh nối đỉnh `u` và `v` với trọng số `w`.
- Sau đó là các truy vấn động:
    - `1 u` – thêm đỉnh `u` vào đồ thị.
    - `2 u v w` – thêm cạnh `(u, v)` với trọng số `w`.
    - `3 s t` – truy vấn đường đi ngắn nhất từ `s` đến `t`.
- Dòng `"END"` báo hiệu kết thúc.

### Output

- Với mỗi truy vấn loại `3`, in ra **độ dài đường đi ngắn nhất** giữa `s` và `t`.
- **Thống kê thời gian chạy** của từng truy vấn.

---

## 🚀 Phân tích cấp độ 1 – Dữ liệu vừa (n ≈ 10^5)

- **Yêu cầu**:
    - `n ≤ 100000`, `m ≤ 100000`.
    - Hỗ trợ thêm đỉnh, cạnh và truy vấn đường đi nhanh.

- **Giải pháp**:
    - Dùng cấu trúc `defaultdict` để lưu danh sách kề.
    - Thuật toán **Dijkstra** với hàng đợi ưu tiên (`heapq`) cho truy vấn đường đi ngắn nhất.

- **Ngôn ngữ**: Python
    - Phù hợp cho phát triển nhanh, xử lý linh hoạt và dễ kiểm tra.

---

## 🚀 Phân tích cấp độ 2 – Dữ liệu lớn (n ≈ 10^7 - 10^8)

- **Yêu cầu**:
    - `n` và `m` có thể lên tới hàng chục triệu.
    - Cần tính toán **phân tán** và hỗ trợ cập nhật đồ thị lớn trong thời gian thực.

- **Không dùng Dijkstra** vì không phù hợp với mô hình phân tán.

- **Giải pháp thay thế**:

    1. **Song song hóa Bellman-Ford**:
        - Cập nhật khoảng cách theo từng lượt (iterative updates).
        - Phù hợp với MapReduce hoặc Spark.

    2. **GraphFrames với Spark**:
        - Cung cấp API dạng Pregel – phù hợp cho đồ thị động lớn.
        - Hỗ trợ thêm/sửa đỉnh cạnh, truy vấn và tính toán hiệu quả.

- **Công nghệ**:
    - Apache Spark
    - PySpark + GraphFrames

---

## 🚀 Phân tích cấp độ 3 – Xử lý Đồ Thị Cực Lớn (Hàng Tỷ Đỉnh/Cạnh)

### ❗ Bài toán mở rộng

Khi quy mô dữ liệu tăng lên tới hàng **tỷ đỉnh và cạnh**, ta không thể xử lý bằng Spark đơn thuần hoặc các thuật toán chạy trên một máy. Việc tính toán cần được chuyển sang cấp độ **xây dựng hệ thống phân tán**, hỗ trợ xử lý **song song**, **batch**, và cả **real-time stream**.

> ⚠️ **Lưu ý**: Phần này chỉ mang tính chất **ý tưởng thiết kế hệ thống**. 

### 🎯 Yêu cầu cấp độ 3:

- Đồ thị có hàng tỷ đỉnh và cạnh, không thể chứa trong bộ nhớ của một máy đơn lẻ.
- Cần hỗ trợ cập nhật liên tục (streaming), không làm gián đoạn hệ thống.
- Truy vấn đường đi ngắn nhất cần phản hồi nhanh (gần real-time).
- Khả năng scale theo chiều ngang (nhiều node máy tính).

---

### ⚙️ Ý tưởng hướng giải quyết

#### 🧩 1. Phân tán dữ liệu – scale horizontally

- Chia đồ thị thành các phân vùng (partitioning).
- Dùng các framework đồ thị phân tán:
  - Apache Spark + GraphFrames/GraphX (Scala)
  - Apache Flink (Gelly)
  - Neo4j Fabric (graph database phân tán)
  - TigerGraph
  - Snap.py
  - cuGraph (nếu dùng GPU)

#### 🚀 2. Kết hợp batch và stream processing

- Dùng Kafka để nhận stream các cập nhật đỉnh/cạnh.
- Apache Flink xử lý các cập nhật này theo thời gian thực.
- Spark hoặc GraphX xử lý các batch truy vấn lớn hoặc định kỳ.

#### 🧠 3. Precompute hoặc heuristic-based

- Với các node quan trọng, precompute đường đi ngắn nhất và lưu lại.
- Với những truy vấn khác, dùng heuristic như A* hoặc landmark labeling để ước lượng nhanh.

---

### 📦 Kiến trúc đề xuất (ý tưởng)

```text
       +---------------------+
       |     Kafka Topic     | <-- Đỉnh, cạnh mới
       +----------+----------+
                  |
             Real-time ingest
                  ↓
           +------+------+
           | Apache Flink | <-- Xử lý stream
           +------+------+
                  ↓
     +------------+-------------+
     | Distributed Graph Storage|
     | (Neo4j Fabric)           |
     +------------+-------------+
                  ↑
       Batch      |
+-----------------+------------------+
|           Spark GraphFrames        | <-- Shortest Path Query
+------------------------------------+
```

----

## 📁 Cấu trúc dự án

```bash
.
├── level_1.py             # Triển khai cấp độ 1 bằng Python
├── level_1.cpp            # Triển khai cấp độ 1 bằng C++
├── level_1.py             # Triển khai cấp độ 2 bằng Python
├── medium_input.txt       # Dữ liệu mẫu với khoảng 10^5 đỉnh cạnh
├── large_input.txt        # Dữ liệu mẫu với khoảng 10^6 đỉnh cạnh
└── README.md              # Tài liệu mô tả
```
