/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import java.util.Locale;

/**
 * Description of an RFC 4566 Session.
 * SDPs are passed as serialized Strings in Java-land and are materialized
 * to SessionDescriptionInterface as appropriate in the JNI layer.
 */
public class SessionDescription {
  /** Java-land enum version of SessionDescriptionInterface's type() string. */
  public static enum Type {
    OFFER,
    PRANSWER,
    ANSWER,
    ROLLBACK;

    public String canonicalForm() {
      return name().toLowerCase(Locale.US);
    }

    @CalledByNative("Type")
    public static Type fromCanonicalForm(String canonical) {
      return Type.valueOf(Type.class, canonical.toUpperCase(Locale.US));
    }
  }

  public final Type type;
  public final String description;

  @CalledByNative
  public SessionDescription(Type type, String description) {
    this.type = type;
    this.description = description;
  }

  @CalledByNative
  String getDescription() {
    return description;
  }

  @CalledByNative
  String getTypeInCanonicalForm() {
    return type.canonicalForm();
  }
}
