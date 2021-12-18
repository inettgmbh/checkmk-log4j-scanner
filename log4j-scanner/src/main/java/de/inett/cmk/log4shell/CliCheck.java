package de.inett.cmk.log4shell;

import com.logpresso.scanner.Log4j2Scanner;

import java.util.LinkedList;
import java.util.List;

public class CliCheck {
    public static void main(String[] cargs) {
        System.out.println("<<<log4j_scanner>>>");
        String[] n_args;
        try {
            switch (cargs.length) {
                case 0:
                    n_args = new String[]{
                            "--scan-log4j1", "--scan-logback", "/"
                    };
                    break;
                case 1:
                    n_args = new String[]{
                            "--scan-log4j1", "--scan-logback", cargs[0]
                    };
                    break;
                default:
                    List<String> t_args = new LinkedList<>();
                    t_args.add("--scan-log4j1");
                    t_args.add("--scan-logback");
                    for (String arg : cargs) {
                        if ( ! (
                                arg.equals("--scan-log4j1")
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
        System.exit(0);
    }
}
