/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.database.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity()
public class DeletedMessage extends AyuMessageBase {
    @PrimaryKey(autoGenerate = true)
    public long fakeId;
}
