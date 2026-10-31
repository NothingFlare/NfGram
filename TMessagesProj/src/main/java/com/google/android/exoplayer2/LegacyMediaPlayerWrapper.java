/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2;

import android.media.MediaPlayer;
import android.os.Looper;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;

/** A {@link Player} wrapper for the legacy Android platform {@link MediaPlayer}. */
public final class LegacyMediaPlayerWrapper extends SimpleBasePlayer {

  private final MediaPlayer player;

  private boolean playWhenReady;

  /**
   * Creates the {@link MediaPlayer} wrapper.
   *
   * @param looper The {@link Looper} used to call all methods on.
   */
  public LegacyMediaPlayerWrapper(Looper looper) {
    super(looper);
    this.player = new MediaPlayer();
  }

  @Override
  protected State getState() {
    return new State.Builder()
        .setAvailableCommands(new Commands.Builder().addAll(Player.COMMAND_PLAY_PAUSE).build())
        .setPlayWhenReady(playWhenReady, Player.PLAY_WHEN_READY_CHANGE_REASON_USER_REQUEST)
        .build();
  }

  @Override
  protected ListenableFuture<?> handleSetPlayWhenReady(boolean playWhenReady) {
    this.playWhenReady = playWhenReady;
    // TODO: Only call these methods if the player is in Started or Paused state.
    if (playWhenReady) {
      player.start();
    } else {
      player.pause();
    }
    return Futures.immediateVoidFuture();
  }
}
