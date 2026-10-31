/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity()
public class DeletedMessageReaction {
    @PrimaryKey(autoGenerate = true)
    public long fakeReactionId;

    public long deletedMessageId;

    public String emoticon;
    public long documentId;
    public boolean isCustom;

    public int count;
    public boolean selfSelected;
}
