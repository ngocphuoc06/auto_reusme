import os
import pandas as pd

# ==== CẤU HÌNH ====
QUERIES_FILE = "random_queries.csv"          # file query random
RESULTS_FILE = "manual_eval_results.csv"     # nơi lưu kết quả
BATCH_SIZE = 20                              # mỗi lần chấm tối đa bao nhiêu query

# ==== 1. Đọc file query random ====
queries = pd.read_csv(QUERIES_FILE)

total_queries = len(queries)
print(f"Tổng số query trong file: {total_queries}")

# ==== 2. Đọc file kết quả nếu đã tồn tại để biết đang ở đâu ====
if os.path.exists(RESULTS_FILE):
    results = pd.read_csv(RESULTS_FILE)
    start_idx = len(results)   # đã chấm được bao nhiêu query
    print(f"Đã chấm {start_idx}/{total_queries} query, sẽ tiếp tục từ query số {start_idx + 1}.")
else:
    results = pd.DataFrame(columns=[
        "row_index", "query_id", "query_text", "num_correct", "score"
    ])
    start_idx = 0
    print("Chưa có file kết quả, bắt đầu chấm từ đầu.")

if start_idx >= total_queries:
    print("Tất cả query đã được chấm rồi!")
    exit()

# ==== 3. Xác định phạm vi batch mới ====
end_idx = min(start_idx + BATCH_SIZE, total_queries)
print(f"Sẽ chấm từ query index {start_idx} đến {end_idx - 1} (tối đa {BATCH_SIZE} query).")

new_rows = []

# ==== 4. Vòng lặp chấm điểm ====
for i in range(start_idx, end_idx):
    row = queries.iloc[i]
    query_id = row.get("query_id", f"row_{i}")
    query_text = row.get("query_text", "")

    print("\n" + "=" * 80)
    print(f"Query số {i + 1}/{total_queries}")
    print(f"query_id: {query_id}")
    print(f"query_text:\n{query_text}")

    # Hỏi người dùng: có bao nhiêu CV đúng trong top-5
    while True:
        user_input = input("Nhập số CV đúng trong top-5 (0-5, hoặc 'q' để dừng sớm): ").strip()

        if user_input.lower() == "q":
            # dừng sớm giữa chừng
            end_idx = i  # để không tính những query chưa nhập
            break

        if user_input.isdigit():
            num_correct = int(user_input)
            if 0 <= num_correct <= 5:
                break

        print("Giá trị không hợp lệ. Hãy nhập số từ 0 đến 5, hoặc 'q' để thoát.")

    if user_input.lower() == "q":
        print("Dừng sớm theo yêu cầu người dùng.")
        break

    score = num_correct / 5.0

    new_rows.append({
        "row_index": i,
        "query_id": query_id,
        "query_text": query_text,
        "num_correct": num_correct,
        "score": score,
    })

# ==== 5. Gộp kết quả cũ + mới, lưu lại ====
if new_rows:
    new_df = pd.DataFrame(new_rows)
    results = pd.concat([results, new_df], ignore_index=True)
    results.to_csv(RESULTS_FILE, index=False)
    print(f"\nĐã lưu {len(new_rows)} kết quả mới.")
    print(f"Tổng cộng đã chấm {len(results)}/{total_queries} query.")
else:
    print("Không có kết quả mới nào được thêm.")
