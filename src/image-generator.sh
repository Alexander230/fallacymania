#!/bin/bash

# Generating pdf images of sheets and stickers for printing
./vector-image-generator.py

# Generating png images for Tabletop Simulator
CARD_W=785
CARD_H=620

HEAD_FONT_SIZE=36
DESC_FONT_SIZE=28
EXAMPLE_FONT_SIZE=23
NUMBER_FONT_SIZE=25
HEAD_FONT=DejaVu-Sans-Bold
DESC_FONT=$HEAD_FONT
EXAMPLE_FONT=Liberation-Sans-Bold-Italic
NUMBER_FONT=$HEAD_FONT

COLORS=($(ls -1 colors/*.png))
LANGUAGES=( rus eng )

rm -rf cards tts
sync
mkdir cards tts

for lang in "${LANGUAGES[@]}"; do
    line_counter=1
    color_counter=0
    while read line; do
        card_file_prefix=cards/$(printf '%02d' $color_counter)-${lang}
        TEXT_COLOR=white
        if [ $color_counter -eq 0 ]; then
	    TEXT_COLOR=black
        fi
        case $line_counter in
            1)
                # Background color
                convert ${COLORS[$color_counter]} -resize ${CARD_W}x${CARD_H}\! ${card_file_prefix}-stage0.png
                # Fallacy name
                convert -background transparent -font $HEAD_FONT -pointsize ${HEAD_FONT_SIZE} -fill $TEXT_COLOR \
                    -gravity center -size ${CARD_W}x80 caption:"$line" ${card_file_prefix}-stage1-text.png
                convert ${card_file_prefix}-stage0.png -page +0+10 ${card_file_prefix}-stage1-text.png \
                    -flatten ${card_file_prefix}-stage1.png
                ;;
            2)
                # Fallacy icon
                convert ${card_file_prefix}-stage1.png -page +10+300 $line -flatten ${card_file_prefix}-stage2.png
                ;;
            3)
                # Fallacy description
                convert -background transparent -font $DESC_FONT -pointsize ${DESC_FONT_SIZE} -fill $TEXT_COLOR \
                    -gravity center -size 735x170 caption:"$line" ${card_file_prefix}-stage3-text.png
                convert ${card_file_prefix}-stage2.png -page +25+110 ${card_file_prefix}-stage3-text.png \
                    -flatten ${card_file_prefix}-stage3.png
                ;;
            4)
                # Fallacy example
                convert -background transparent -font $EXAMPLE_FONT -pointsize ${EXAMPLE_FONT_SIZE} \
                    -fill $TEXT_COLOR -gravity center -size 380x360 caption:"$line" ${card_file_prefix}-stage4-text.png
                convert ${card_file_prefix}-stage3.png -page +315+270 ${card_file_prefix}-stage4-text.png \
                    -flatten ${card_file_prefix}-stage4.png
                # Fallacy number
                convert -background transparent -font $NUMBER_FONT -pointsize ${NUMBER_FONT_SIZE} -fill $TEXT_COLOR \
                    -gravity center -size 40x30 caption:"$color_counter" ${card_file_prefix}-number.png
                convert ${card_file_prefix}-stage4.png -page +740+580 ${card_file_prefix}-number.png \
                    -flatten ${card_file_prefix}-final.png
                ;;
        esac
        ((line_counter++))
        if [ $line_counter -eq 5 ]; then
            line_counter=1
            ((color_counter++))
        fi
    done < fallacies-${lang}.txt
    # Sheet montage
    fallacies=$(ls -1 cards/???${lang}-final.png)
    sheet=tts/fallacies-${lang}.png
    montage ${fallacies} -tile 1x9 -geometry +0+0 miff:- | montage - -geometry +0+0 -tile 5x1 ${sheet}
    # Cards montage
    cards=tts/cards-${lang}.png
    montage ${fallacies} -tile 10x5 -geometry +0+0 ${cards}
done
