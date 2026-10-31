/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import android.os.Bundle;
import android.os.Parcel;
import com.google.android.exoplayer2.util.BundleableUtil;
import java.util.ArrayList;
import java.util.List;

/** Encodes data that can be decoded by {@link CueDecoder}. */
public final class CueEncoder {
  /**
   * Encodes an {@link List} of {@link Cue} to a byte array that can be decoded by {@link
   * CueDecoder}.
   *
   * @param cues Cues to be encoded.
   * @return The serialized byte array.
   */
  public byte[] encode(List<Cue> cues) {
    ArrayList<Bundle> bundledCues = BundleableUtil.toBundleArrayList(cues);
    Bundle allCuesBundle = new Bundle();
    allCuesBundle.putParcelableArrayList(CueDecoder.BUNDLED_CUES, bundledCues);
    Parcel parcel = Parcel.obtain();
    parcel.writeBundle(allCuesBundle);
    byte[] bytes = parcel.marshall();
    parcel.recycle();

    return bytes;
  }
}
