/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import android.opengl.EGLContext;
import android.view.Surface;

/** EGL 1.4 implementation of EglBase. */
public interface EglBase14 extends EglBase {

  interface Context extends EglBase.Context {
    EGLContext getRawContext();
  }
}
