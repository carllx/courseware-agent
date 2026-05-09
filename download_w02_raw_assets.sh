#!/bin/bash
# 在宿主机（非沙盒环境）运行此脚本以下载视觉素材

# 目标目录
DEST_DIR="交互产品开发/weeks/W02_Cognitive_Friction/public/assets"
mkdir -p "$DEST_DIR"

echo "开始下载真实视觉素材到 $DEST_DIR..."

curl -L "https://images.squarespace-cdn.com/content/v1/5fed55498500a82fe9d2f441/1671745902478-DSHZY894DHGZX15L333O/Don+Norman.png" -o "$DEST_DIR/don_norman.png"
curl -L "https://taschen.makaira.media/taschen/image/upload/f_webp,w_1200/v1743586233/products-live/04ceea02f569b520bf04fddfa6256faf.png" -o "$DEST_DIR/apollo_1202.png"
curl -L "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSiVnmz5_1xmdYp-Ce8tjJPbTExMC9tIJQvTg&s" -o "$DEST_DIR/therac_25.jpg"
curl -L "https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/JXKYR7SXGEI6TKUDKBHQQ27V2Y.jpg" -o "$DEST_DIR/boeing_mcas.jpg"
curl -L "https://www.worldiaday.org/sites/default/files/styles/persons_list_profile_picture/public/images/2019-02/AlanCooper.jpg?itok=1RTmCNV8" -o "$DEST_DIR/alan_cooper.jpg"
curl -L "https://media.wiley.com/product_data/coverImage300/71/11187665/1118766571.jpg" -o "$DEST_DIR/about_face_cover.jpg"

echo "下载完成！"
curl -L "https://i.dailymail.co.uk/i/pix/2017/02/28/20/3DD00D7F00000578-4268850-image-a-11_1488314413889.jpg" -o "$DEST_DIR/aws_status.jpg"
curl -L "https://i.dailymail.co.uk/i/pix/2017/02/28/20/3DD00D7F00000578-4268850-image-a-11_1488314413889.jpg" -o "交互产品开发/weeks/W02_Cognitive_Friction/public/slides/w02-slide-10c2.jpg"
