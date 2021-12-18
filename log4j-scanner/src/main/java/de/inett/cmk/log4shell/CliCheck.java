package de.inett.cmk.log4shell;

import com.logpresso.scanner.Log4j2Scanner;

import java.util.Arrays;
import java.util.List;

public class CliCheck {
    public static void main(String[] cargs) {
        String[] n_args;
        switch (cargs.length) {
            case 0:
                n_args = new String[]{"/", "--scan-log4j1"};
                break;
            case 1:
                n_args = new String[]{cargs[0], "--scan-log4j1"};
                break;
            default:
                List<String> t_args = Arrays.asList(cargs);
                if (! t_args.contains("--scan-log4j1")) {
                    t_args.add("--scan-log4j1");
                }
                n_args = t_args.toArray(new String[0]);
                break;
        }
        System.out.println("<<<log4j_scanner>>>");
        try {
            Log4j2Scanner scanner = new Log4j2Scanner();
            scanner.run(n_args);
            System.exit(0);
        } catch (Throwable t) {
            System.out.println("Error: " + t.getMessage());
            System.exit(-1);
        }
    }
}
