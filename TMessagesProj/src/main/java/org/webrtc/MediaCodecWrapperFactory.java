/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import java.io.IOException;

interface MediaCodecWrapperFactory {
  /**
   * Creates a new {@link MediaCodecWrapper} by codec name.
   *
   * <p>For additional information see {@link android.media.MediaCodec#createByCodecName}.
   */
  MediaCodecWrapper createByCodecName(String name) throws IOException;
}
