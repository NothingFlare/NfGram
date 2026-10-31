/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata.vorbis;

import android.os.Parcel;

/** A vorbis comment, extracted from a FLAC or Ogg file. */
@SuppressWarnings("deprecation") // Extending deprecated type for backwards compatibility.
public final class VorbisComment extends com.google.android.exoplayer2.metadata.flac.VorbisComment {

  /**
   * @param key The key.
   * @param value The value.
   */
  public VorbisComment(String key, String value) {
    super(key, value);
  }

  /* package */ VorbisComment(Parcel in) {
    super(in);
  }

  public static final Creator<VorbisComment> CREATOR =
      new Creator<VorbisComment>() {

        @Override
        public VorbisComment createFromParcel(Parcel in) {
          return new VorbisComment(in);
        }

        @Override
        public VorbisComment[] newArray(int size) {
          return new VorbisComment[size];
        }
      };
}
