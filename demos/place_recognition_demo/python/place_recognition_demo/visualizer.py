"""
 Copyright (c) 2021-2024 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import numpy as np
import cv2

SIZE = 200
BLACK = (0, 0, 0)
LWD = 2
TEXT_SIZE = 1.5
BORDER = 30


def add_top10_gallery_images(demo_image, impaths, distances, input_image):
    """ Add top-10 most similar images from the gallery to demo image. """

    for index, impath in enumerate(impaths[:10]):
        image = cv2.imread(impath)
        image = cv2.resize(image, (SIZE, SIZE))

        h_shift = 2 * BORDER + input_image.shape[0] + (SIZE + BORDER) * (index // 5)
        w_shift = BORDER + (index % 5) * (SIZE + BORDER)

        demo_image[h_shift: h_shift + SIZE, w_shift: w_shift + SIZE] = image

        if distances is not None:
            cv2.putText(demo_image, '{}:{}'.format(index, int(distances[index] * 100) / 100),
                        (w_shift - BORDER, h_shift - 5), 1,
                        TEXT_SIZE, BLACK, LWD)
        else:
            cv2.putText(demo_image, '{}'.format(index), (w_shift - BORDER, h_shift - 5), 1,
                        TEXT_SIZE, BLACK, LWD)

    return demo_image


def visualize(image, impaths, distances, input_size, compute_embedding_time,
              search_in_gallery_time, imshow_delay, presenter, no_show=False):
    """ Visualizes input frame and top-10 most similar images from the gallery. """

    input_image = cv2.resize(image, (SIZE * 4, SIZE * 3))

    demo_image = np.ones(
        (input_image.shape[0] + SIZE * 2 + BORDER * 4, SIZE * 5 + BORDER * 6, 3),
        dtype=np.uint8) * 200

    presenter.drawGraphs(input_image)

    demo_image[BORDER:BORDER + input_image.shape[0],
               BORDER:BORDER + input_image.shape[1]] = input_image

    cv2.putText(demo_image, 'Gallery size: {}'.format(len(impaths)),
                (BORDER * 2 + input_image.shape[1], BORDER * 2 + 30), 1, TEXT_SIZE, BLACK, LWD)
    if not np.isnan(compute_embedding_time):
        cv2.putText(demo_image,
                    'Embbeding (ms): {}'.format(int(compute_embedding_time * 10000) / 10.0),
                    (BORDER * 2 + input_image.shape[1], BORDER * 2 + 60), 1, TEXT_SIZE, BLACK, LWD)
    if not np.isnan(search_in_gallery_time):
        cv2.putText(demo_image,
                    'Gallery search (ms): {}'.format(int(search_in_gallery_time * 10000) / 10.0),
                    (BORDER * 2 + input_image.shape[1], BORDER * 2 + 90), 1, TEXT_SIZE, BLACK, LWD)

    cv2.putText(demo_image, 'Inp. res: {}x{}'.format(input_size[0], input_size[1]),
                (BORDER * 2 + input_image.shape[1], BORDER * 2 + 120), 1, TEXT_SIZE, BLACK, LWD)

    demo_image = add_top10_gallery_images(demo_image, impaths, distances, input_image)

    if not no_show:
        cv2.imshow('demo_image', demo_image)
        key_pressed = cv2.waitKey(imshow_delay)
        presenter.handleKey(key_pressed)
        return (demo_image, key_pressed & 0xff) if key_pressed != -1 else (demo_image, -1)

    return (demo_image, -1)
