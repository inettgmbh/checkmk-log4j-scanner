package de.inett.cmk.log4shell;

import java.security.Permission;

public class TrapExitSecurityManager extends SecurityManager {

    @Override
    public void checkPermission(Permission perm) {
    }

    @Override
    public void checkExit(int status) {
        super.checkExit(status);
        throw new ExitTrappedException();
    }
}
