/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.metadata.dvbsi;

import android.os.Parcel;
import android.os.Parcelable;
import com.google.android.exoplayer2.metadata.Metadata;
import com.google.android.exoplayer2.util.Assertions;

/**
 * A representation of a DVB Application Information Table (AIT).
 *
 * <p>For more info on the AIT see section 5.3.4 of the <a
 * href="https://www.etsi.org/deliver/etsi_ts/102800_102899/102809/01.01.01_60/ts_102809v010101p.pdf">
 * DVB ETSI TS 102 809 v1.1.1 spec</a>.
 */
public final class AppInfoTable implements Metadata.Entry {
  /**
   * The application shall be started when the service is selected, unless the application is
   * already running.
   */
  public static final int CONTROL_CODE_AUTOSTART = 0x01;
  /**
   * The application is allowed to run while the service is selected, however it shall not start
   * automatically when the service becomes selected.
   */
  public static final int CONTROL_CODE_PRESENT = 0x02;

  public final int controlCode;
  public final String url;

  public AppInfoTable(int controlCode, String url) {
    this.controlCode = controlCode;
    this.url = url;
  }

  @Override
  public String toString() {
    return "Ait(controlCode=" + controlCode + ",url=" + url + ")";
  }

  @Override
  public int describeContents() {
    return 0;
  }

  @Override
  public void writeToParcel(Parcel parcel, int i) {
    parcel.writeString(url);
    parcel.writeInt(controlCode);
  }

  public static final Parcelable.Creator<AppInfoTable> CREATOR =
      new Parcelable.Creator<AppInfoTable>() {
        @Override
        public AppInfoTable createFromParcel(Parcel in) {
          String url = Assertions.checkNotNull(in.readString());
          int controlCode = in.readInt();
          return new AppInfoTable(controlCode, url);
        }

        @Override
        public AppInfoTable[] newArray(int size) {
          return new AppInfoTable[size];
        }
      };
}
