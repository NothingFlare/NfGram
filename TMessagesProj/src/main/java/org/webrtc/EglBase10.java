/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import javax.microedition.khronos.egl.EGLContext;

/** EGL 1.0 implementation of EglBase. */
public interface EglBase10 extends EglBase {
  interface Context extends EglBase.Context {
    EGLContext getRawContext();
  }
}
