#!/bin/bash
CARD_W=785
CARD_H=620
STICKER_W=785
STICKER_H=1222
HEAD_FONT_SIZE=36
DESC_FONT_SIZE=28
EXAMPLE_FONT_SIZE=23
NUMBER_FONT_SIZE=25
COLORS=($(ls -1 colors/*.png))
LANGUAGES=( rus eng )
for lang in "${LANGUAGES[@]}"; do
    rm -rf cards-${lang} stickers-${lang} tts-${lang}
    sync
    mkdir cards-${lang} stickers-${lang} tts-${lang}
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
                convert -background transparent -font DejaVu-Sans-Bold -pointsize ${HEAD_FONT_SIZE} -fill white \
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
                convert -background transparent -font DejaVu-Sans-Bold -pointsize ${DESC_FONT_SIZE} -fill white \
                    -gravity center -size 735x170 caption:"$line" ${card_file_prefix}-stage3-text.png
                convert ${card_file_prefix}-stage2.png -page +25+110 ${card_file_prefix}-stage3-text.png \
                    -flatten ${card_file_prefix}-stage3.png
                ;;
            4)
                # Fallacy example
                convert -background transparent -font Liberation-Sans-Bold-Italic -pointsize ${EXAMPLE_FONT_SIZE} \
                    -fill white -gravity center -size 380x360 caption:"$line" ${card_file_prefix}-stage4-text.png
                convert ${card_file_prefix}-stage3.png -page +315+270 ${card_file_prefix}-stage4-text.png \
                    -flatten ${card_file_prefix}-stage4.png
                # Fallacy number
                convert -background transparent -font DejaVu-Sans-Bold -pointsize ${NUMBER_FONT_SIZE} -fill white \
                    -gravity center -size 40x30 caption:"$color_counter" ${card_file_prefix}-number.png
                convert ${card_file_prefix}-stage4.png -page +740+580 ${card_file_prefix}-number.png \
                    -flatten ${card_file_prefix}-final.png
                # Sticker
                convert ${COLORS[$color_counter]} -resize ${STICKER_W}x${STICKER_H}\! ${sticker_file_prefix}-stage0.png
                composite -gravity center ${card_file_prefix}-stage4.png ${sticker_file_prefix}-stage0.png \
                    ${sticker_file_prefix}-stage1.png
                convert ${sticker_file_prefix}-stage1.png -page +735+1178 ${card_file_prefix}-number.png \
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
    montage_list=$(ls -1 cards-${lang}/*-final.png)
    montage ${montage_list} -tile 1x9 -geometry +0+0 miff:- | montage - -geometry +0+0 -tile 5x1 fallacies-${lang}.png
    # Tabletop Simulator resources montage
    tts_file_prefix=tts-${lang}/fallacies-tts
    montage_list_tts_deck=$(ls -1 cards-${lang}/*-final.png)
    montage ${montage_list_tts_deck} -tile 10x5 -geometry +0+0 tts-${lang}/fallacies-tts-deck-${lang}.png
    # Stickers montage
    montage_list_single=$(ls -1 stickers-${lang}/*-final.png)
    montage_list_double=$(for item in $montage_list_single; do echo $item; echo $item; done)
    montage $montage_list_single -tile 5x5 -geometry +10+10 stickers-${lang}/stickers-single-${lang}-tile.png
    montage $montage_list_double -tile 5x5 -geometry +10+10 stickers-${lang}/stickers-double-${lang}-tile.png
done
