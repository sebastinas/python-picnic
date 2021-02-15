/*
 * Copyright 2021 Sebastian Ramacher <sebastian.ramacher@ait.ac.at>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#ifndef PYPICNIC_HELPER_FUNCTIONS_H
#define PYPICNIC_HELPER_FUNCTIONS_H

#include <picnic.h>

static size_t picnic_private_key_size(picnic_params_t parameters) {
  switch (parameters) {
  case Picnic_L1_FS:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L1_FS);
  case Picnic_L1_UR:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L1_UR);
  case Picnic_L3_FS:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L3_FS);
  case Picnic_L3_UR:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L3_UR);
  case Picnic_L5_FS:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L5_FS);
  case Picnic_L5_UR:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L5_UR);
  case Picnic3_L1:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic3_L1);
  case Picnic3_L3:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic3_L3);
  case Picnic3_L5:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic3_L5);
  case Picnic_L1_full:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L1_full);
  case Picnic_L3_full:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L3_full);
  case Picnic_L5_full:
    return PICNIC_PRIVATE_KEY_SIZE(Picnic_L5_full);
  default:
    return 0;
  }
}

static size_t picnic_public_key_size(picnic_params_t parameters) {
  switch (parameters) {
  case Picnic_L1_FS:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L1_FS);
  case Picnic_L1_UR:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L1_UR);
  case Picnic_L3_FS:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L3_FS);
  case Picnic_L3_UR:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L3_UR);
  case Picnic_L5_FS:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L5_FS);
  case Picnic_L5_UR:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L5_UR);
  case Picnic3_L1:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic3_L1);
  case Picnic3_L3:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic3_L3);
  case Picnic3_L5:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic3_L5);
  case Picnic_L1_full:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L1_full);
  case Picnic_L3_full:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L3_full);
  case Picnic_L5_full:
    return PICNIC_PUBLIC_KEY_SIZE(Picnic_L5_full);
  default:
    return 0;
  }
}

#endif
