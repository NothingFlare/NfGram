/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import android.content.Context;

public interface NetworkChangeDetectorFactory {
  public NetworkChangeDetector create(NetworkChangeDetector.Observer observer, Context context);
}
