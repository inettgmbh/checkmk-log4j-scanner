package de.inett.cmk.log4shell;

import com.logpresso.scanner.Log4j2Scanner;

import java.util.LinkedList;
import java.util.List;

public class CliCheck {
    private static SecurityManager sm_orig;
    private static SecurityManager sm_new = new TrapExitSecurityManager();

    public static void main(String[] cargs) {
        System.out.println("<<<log4j_scanner>>>");

        // Don't quit on System.exit()
        sm_orig = System.getSecurityManager();
        System.setSecurityManager(sm_new);

        String[] n_args;
        try {
            switch (cargs.length) {
                case 0:
                    n_args = new String[]{
                            "--scan-zip", "--scan-logback", "/"
                    };
                    break;
                case 1:
                    n_args = new String[]{
                            "--scan-log4j1", "--scan-logback", cargs[0]
                    };
                    break;
                default:
                    List<String> t_args = new LinkedList<>();
                    t_args.add("--scan-zip");
                    t_args.add("--scan-logback");
                    for (String arg : cargs) {
                        if ( ! (
                                arg.equals("--scan-zip")
                                || arg.equals("--scan-logback")
                        )) {
                            t_args.add(arg);
                        }
                    }
                    n_args = t_args.toArray(new String[0]);
                    break;
            }
            Log4j2Scanner scanner = new Log4j2Scanner();
            scanner.run(n_args);
        } catch (Throwable t) {
            System.out.println("Error: " + t.getMessage());
        }

        // Now quit on System.exit(int)
        System.setSecurityManager(sm_orig);

        System.exit(0);
    }
}
