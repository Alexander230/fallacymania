#!/bin/bash
export CARD_W=785
export CARD_H=620
export STICKER_W=700
export STICKER_H=1090
export COLORS=($(ls -1 colors/*.png))
export LANGUAGES=( rus eng )
for lang in "${LANGUAGES[@]}"; do
    rm -rf cards-${lang} stickers-${lang}
    sync
    mkdir cards-${lang} stickers-${lang}
    line_counter=1
    color_counter=0
    while read line; do
        card_file_prefix=cards-${lang}/$(printf '%02d' $color_counter)
        sticker_file_prefix=stickers-${lang}/$(printf '%02d' $color_counter)
        case $line_counter in
            1)
                # Background color
                convert ${COLORS[$color_counter]} -resize ${CARD_W}x${CARD_H}\! ${card_file_prefix}-stage0.png
                # Fallacy name
                convert -background transparent -font DejaVu-Sans-Bold -pointsize 35 -fill white -gravity center \
                    label:"$line" ${card_file_prefix}-stage1-text.png
                convert ${card_file_prefix}-stage1-text.png -gravity center -background transparent \
                    -extent ${CARD_W}x80 ${card_file_prefix}-stage1-resized.png
                convert ${card_file_prefix}-stage0.png -page +0+10 ${card_file_prefix}-stage1-resized.png \
                    -flatten ${card_file_prefix}-stage1.png
                ;;
            2)
                # Fallacy icon
                convert $line -filter Lanczos -distort Resize 300x300 ${card_file_prefix}-icon-resized.png
                convert ${card_file_prefix}-stage1.png -page +10+300 ${card_file_prefix}-icon-resized.png \
                    -flatten ${card_file_prefix}-stage2.png
                ;;
            3)
                # Fallacy description
                convert -background transparent -font DejaVu-Sans-Bold -pointsize 25 -fill white -gravity center \
                    label:"$line" ${card_file_prefix}-stage3-text.png
                convert ${card_file_prefix}-stage3-text.png -gravity north -background transparent \
                    -extent 735x160 ${card_file_prefix}-stage3-resized.png
                convert ${card_file_prefix}-stage2.png -page +25+130 ${card_file_prefix}-stage3-resized.png \
                    -flatten ${card_file_prefix}-stage3.png
                ;;
            4)
                # Fallacy example
                convert -background transparent -font Liberation-Sans-Bold-Italic -pointsize 18 -fill white \
                    -gravity center label:"$line" ${card_file_prefix}-stage4-text.png
                convert ${card_file_prefix}-stage4-text.png -gravity north -background transparent \
                    -extent 340x360 ${card_file_prefix}-stage4-resized.png
                convert ${card_file_prefix}-stage3.png -page +315+320 ${card_file_prefix}-stage4-resized.png \
                    -flatten ${card_file_prefix}-stage4.png
                # Fallacy number
                convert -background transparent -font DejaVu-Sans-Bold -pointsize 25 -fill white -gravity center \
                    label:"$color_counter" ${card_file_prefix}-number.png
                convert ${card_file_prefix}-number.png -gravity center -background transparent \
                    -extent 40x30 ${card_file_prefix}-number-resized.png
                convert ${card_file_prefix}-stage4.png -page +740+580 ${card_file_prefix}-number-resized.png \
                    -flatten ${card_file_prefix}-final.png
                # Sticker
                convert ${COLORS[$color_counter]} -resize ${STICKER_W}x${STICKER_H}\! ${sticker_file_prefix}-stage0.png
                convert ${card_file_prefix}-stage4.png -filter Lanczos -distort Resize ${STICKER_W}x \
                    ${sticker_file_prefix}-stage1.png
                composite -gravity center ${sticker_file_prefix}-stage1.png ${sticker_file_prefix}-stage0.png \
                    ${sticker_file_prefix}-stage2.png
                convert ${sticker_file_prefix}-stage2.png -page +655+1050 ${card_file_prefix}-number-resized.png \
                    -flatten ${sticker_file_prefix}-final.png
                ;;
        esac
        ((line_counter++))
        if [ $line_counter -eq 5 ]; then
            line_counter=1
            ((color_counter++))
        fi
    done < fallacies-${lang}.txt
    # Sheet montage
    rm -f fallacies-${lang}.png
    montage_list=$(ls -1 cards-${lang}/*-final.png | grep -v 00-)
    montage ${montage_list} -tile 1x9 -geometry +0+0 miff:- | montage - -geometry +0+0 -tile 5x1 fallacies-${lang}.png
    # Stickers montage
    montage_list_single=$(ls -1 stickers-${lang}/*-final.png)
    montage_list_double=$(for item in $montage_list_single; do echo $item; echo $item; done)
    montage $montage_list_double -tile 5x5 -geometry +10+10 stickers-${lang}/stickers-${lang}-tile.png
done
