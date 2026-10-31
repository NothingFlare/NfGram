/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.database.entities;

import androidx.room.Embedded;
import androidx.room.Relation;

import java.util.List;

public class DeletedMessageFull {
    @Embedded
    public DeletedMessage message;

    @Relation(
            parentColumn = "fakeId",
            entityColumn = "deletedMessageId"
    )
    public List<DeletedMessageReaction> reactions;
}
