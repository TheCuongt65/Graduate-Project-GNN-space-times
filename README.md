# Ứng dụng mạng nơ-ron đồ thị trong dự báo chất lượng không khí theo không gian và thời gian

## Tóm tắt

Đề tài tập trung nghiên cứu bài toán dự đoán mức độ ô nhiễm không khí, đặc biệt
là các hạt mịn PM2.5, trên phạm vi toàn cầu và tập trung ở các quốc gia đang phát
triển. Điều này đòi hỏi sự xem xét kỹ lưỡng về nhiều yếu tố ảnh hưởng khác nhau
trong khoảng thời gian dài, trong đó gió là một yếu tố quan trọng. Với đề tài này,
chúng tôi đã sử dụng mạng đồ thị Graph Neural Networks (GNNs) để tái cấu trúc
không gian địa lý phản ánh mối quan hệ giữa các trạm đo. Đồng thời, kết hợp với
mạng hồi quy (GRUs) cung cấp cho chúng tôi khả năng tạo ra một cấu trúc không
gian - thời gian để nghiên cứu sâu hơn về ảnh hưởng của gió. Kết quả đạt được là
chúng tôi có thể dự đoán chất lượng không khí ở các thời điểm tiếp theo ở những
khu vực khác nhau dưới tác động của gió.

## Tổng quan phương pháp

Dự án này sử dụng một mô hình tương tự T-GCN, tuy nhiên, ở phần GCN, chúng tôi cải thiện nó thay thế bằng mô hình đề xuất của chúng tôi là PM2.5-GNN

![alt](/image%20cap%20màn/slide_image/Đồ%20thị%20dự%20báo%20không%20gian%20và%20thời%20gian..png)

### Dữ liệu

Dữ liệu trong 4 năm (01/01/2015 - 31/12/2018) được thu thập từ hai nguồn: 
* Ủy ban khí tượng Tầm trung Châu Âu 
* Bộ sinh thái môi trường Trung Quốc.

### Kịch bản thực nghiệm

Dữ liệu được phân chia theo các năm hoặc theo các quý và theo các tháng
Chúng tôi chia dữ liệu thành 3 phần train, val và test. 

Như vậy chúng tôi có kịch bản xây dựng mô hình như bảng sau:

| Kịch bản | Train         | Val           | Test |
|----------|---------------|---------------|------|
| 1        | Dòng 1, cột 2 | Dòng 1, cột 3 |      |
| 2        | Dòng 2, cột 2 | Dòng 2, cột 3 |      |
| 3        |               |               |      |

Để đồng nhất về thông tin lịch sử của mỗi mẫu dữ liệu.

Các mẫu dữ liệu sẽ lấy 1 giờ đầu tiên làm đầu vào dự đoán cho 24 giờ tiếp theo, với dữ liệu về khí tượng được cập nhật liên tục.

# Kết quả

### Đánh giá

#### Kết quả thu được như sau

| Kịch bản | MSE           | POS           |
|----------|---------------|---------------|
| 1        | Dòng 1, cột 2 | Dòng 1, cột 3 |     
| 2        | Dòng 2, cột 2 | Dòng 2, cột 3 |      
| 3        |               |               |      

#### Biều đồ biến động 
(Lưu ý: Do có sự nhầm lẫn đánh máy nên đường màu xanh là đường Predict và đường màu đỏ là đường Ground truth)

![alt](image%20cap%20màn/result/gif/giff.gif)

### Trực quan kết quả


[![Watch the video](https://img.youtube.com/vi/yf3dzKN2ecI/maxresdefault.jpg)](https://youtu.be/yf3dzKN2ecI)

# Hướng dẫn deploy app 
    * Cài đặt WSL2 với distros Ubuntu-22.04
    * Cài đặt Python 3.10 
    * Cài đặt Pytorch-GPU (Hoặc CPU)
    * Cài đặt các phụ thuộc bằng lệnh pip install requirements.txt
    * cd vào web, chạy lệnh streamlit run app.py

# Các nguồn tham khảo

# Thực hiện
