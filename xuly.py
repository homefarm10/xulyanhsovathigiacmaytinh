import os

# mapping id cũ -> id mới
mapping = {
    # 0: 0,   # Using_phone
    # 4: 1,   # hand-raising
    # 8: 2    # sleep
    3: 0,   # Using_phone
    2: 2    # sleep
}

def process_dataset(base_path):
    for split in ["train", "valid", "test"]:
        label_dir = os.path.join(base_path, split, "labels")
        image_dir = os.path.join(base_path, split, "images")

        for file in os.listdir(label_dir):
            label_path = os.path.join(label_dir, file)

            with open(label_path, 'r') as f:
                lines = f.readlines()

            new_lines = []

            for line in lines:
                parts = line.strip().split()
                class_id = int(parts[0])

                if class_id in mapping:
                    parts[0] = str(mapping[class_id])
                    new_lines.append(" ".join(parts))

            # lấy tên ảnh tương ứng
            image_name = os.path.splitext(file)[0]

            # tìm ảnh (.jpg / .png)
            image_path = None
            for ext in [".jpg", ".png", ".jpeg"]:
                temp_path = os.path.join(image_dir, image_name + ext)
                if os.path.exists(temp_path):
                    image_path = temp_path
                    break

            # ❌ nếu không còn object hợp lệ → xóa cả ảnh + label
            if len(new_lines) == 0:
                os.remove(label_path)
                if image_path:
                    os.remove(image_path)
                print(f"Deleted: {file}")
            else:
                # ✔️ ghi lại label mới
                with open(label_path, 'w') as f:
                    f.write("\n".join(new_lines))

    print("Done!")


# chạy
process_dataset(r"Action Behaviour Student")

# dem so luong
# import os
from collections import Counter

# tên class của bạn (sau khi đã lọc còn 3 class)
names = ['Using_phone', 'hand-raising', 'sleep']

def count_dataset(base_path):
    for split in ["train", "valid", "test"]:
        label_dir = os.path.join(base_path, split, "labels")
        image_dir = os.path.join(base_path, split, "images")

        total_images = len(os.listdir(image_dir))
        class_counter = Counter()

        for file in os.listdir(label_dir):
            path = os.path.join(label_dir, file)

            with open(path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                class_id = int(line.split()[0])
                class_counter[class_id] += 1

        print(f"\n===== {split.upper()} =====")
        print(f"Total images: {total_images}")

        for i in range(len(names)):
            print(f"{names[i]}: {class_counter[i]} objects")
count_dataset("Action Behaviour Student")