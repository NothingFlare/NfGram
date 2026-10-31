/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import java.nio.ByteBuffer;

/** Class with static JNI helper functions that are used in many places. */
public class JniCommon {
  /** Functions to increment/decrement an rtc::RefCountInterface pointer. */
  public static native void nativeAddRef(long refCountedPointer);
  public static native void nativeReleaseRef(long refCountedPointer);

  public static native ByteBuffer nativeAllocateByteBuffer(int size);
  public static native void nativeFreeByteBuffer(ByteBuffer buffer);
}
