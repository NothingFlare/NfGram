/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor.avi;

/**
 * A chunk, as defined in the AVI spec.
 *
 * <p>See https://docs.microsoft.com/en-us/windows/win32/directshow/avi-riff-file-reference.
 */
/* package */ interface AviChunk {

  /** Returns the chunk type fourcc. */
  int getType();
}
