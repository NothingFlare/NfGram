/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import static com.google.android.exoplayer2.util.Assertions.checkArgument;

/** Value class specifying information about a decoded video frame. */
public class FrameInfo {
  /** The width of the frame, in pixels. */
  public final int width;
  /** The height of the frame, in pixels. */
  public final int height;
  /** The ratio of width over height for each pixel. */
  public final float pixelWidthHeightRatio;
  /**
   * An offset in microseconds that is part of the input timestamps and should be ignored for
   * processing but added back to the output timestamps.
   *
   * <p>The offset stays constant within a stream but changes in between streams to ensure that
   * frame timestamps are always monotonically increasing.
   */
  public final long streamOffsetUs;

  // TODO(b/227624622): Add color space information for HDR.

  /**
   * Creates a new instance.
   *
   * @param width The width of the frame, in pixels.
   * @param height The height of the frame, in pixels.
   * @param pixelWidthHeightRatio The ratio of width over height for each pixel.
   * @param streamOffsetUs An offset in microseconds that is part of the input timestamps and should
   *     be ignored for processing but added back to the output timestamps.
   */
  public FrameInfo(int width, int height, float pixelWidthHeightRatio, long streamOffsetUs) {
    checkArgument(width > 0, "width must be positive, but is: " + width);
    checkArgument(height > 0, "height must be positive, but is: " + height);

    this.width = width;
    this.height = height;
    this.pixelWidthHeightRatio = pixelWidthHeightRatio;
    this.streamOffsetUs = streamOffsetUs;
  }
}
