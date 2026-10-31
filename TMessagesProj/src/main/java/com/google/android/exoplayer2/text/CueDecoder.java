/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import android.os.Bundle;
import android.os.Parcel;
import com.google.android.exoplayer2.util.Assertions;
import com.google.android.exoplayer2.util.BundleableUtil;
import com.google.common.collect.ImmutableList;
import java.util.ArrayList;

/** Decodes data encoded by {@link CueEncoder}. */
public final class CueDecoder {

  // key under which list of cues is saved in the bundle
  static final String BUNDLED_CUES = "c";

  /**
   * Decodes byte array into list of {@link Cue} objects.
   *
   * @param bytes byte array produced by {@link CueEncoder}
   * @return decoded list of {@link Cue} objects.
   */
  public ImmutableList<Cue> decode(byte[] bytes) {
    Parcel parcel = Parcel.obtain();
    parcel.unmarshall(bytes, 0, bytes.length);
    parcel.setDataPosition(0);
    Bundle bundle = parcel.readBundle(Bundle.class.getClassLoader());
    parcel.recycle();
    ArrayList<Bundle> bundledCues =
        Assertions.checkNotNull(bundle.getParcelableArrayList(BUNDLED_CUES));

    return BundleableUtil.fromBundleList(Cue.CREATOR, bundledCues);
  }
}
