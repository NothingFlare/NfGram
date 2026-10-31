/*
 * Copyright (C) Odysseus Software GmbH
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger.audioinfo.m4a;

import org.telegram.messenger.audioinfo.util.PositionInputStream;

import java.io.IOException;
import java.io.InputStream;

public final class MP4Input extends MP4Box<PositionInputStream> {

	public MP4Input(InputStream delegate) {
		super(new PositionInputStream(delegate), null, "");
	}

	public MP4Atom nextChildUpTo(String expectedTypeExpression) throws IOException {
		while (true) {
			MP4Atom atom = nextChild();
			if (atom.getType().matches(expectedTypeExpression)) {
				return atom;
			}
		}
	}

	public String toString() {
		return "mp4[pos=" + getPosition() + "]";
	}
}
