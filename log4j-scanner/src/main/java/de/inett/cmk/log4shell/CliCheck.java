package de.inett.cmk.log4shell;

import com.logpresso.scanner.Configuration;
import com.logpresso.scanner.Log4j2Scanner;
import com.logpresso.scanner.Metrics;

import java.lang.reflect.Field;
import java.util.LinkedList;
import java.util.List;

public class CliCheck extends Log4j2Scanner {

    public static void main(String[] args) {
        System.out.println("<<<log4j_scanner>>>");
        String[] n_args = prepareArguments(args);
        try {
            Log4j2Scanner scanner = new CliCheck();
            scanner.run(n_args);
        } catch (Throwable t) {
            System.out.println("Error: " + t.getMessage());
        }
        System.exit(0);
    }

    /**
     * This is a hack, don't change
     */
    @Override
    public int run(String[] args) throws Exception {
        Field config = Log4j2Scanner.class.getDeclaredField("config");
        config.setAccessible(true);
        config.set(this, Configuration.parseArguments(args));

        Field metrics = Log4j2Scanner.class.getDeclaredField("metrics");
        metrics.setAccessible(true);
        metrics.set(this, new Metrics());

        return scanAndFix();
    }

    private static String[] prepareArguments(String[] cargs) {
        String[] ret;
        switch (cargs.length) {
            case 0:
                ret = new String[]{
                        "--scan-zip", "--scan-logback", "/"
                };
                break;
            case 1:
                ret = new String[]{
                        "--scan-log4j1", "--scan-logback", cargs[0]
                };
                break;
            default:
                List<String> t_args = new LinkedList<>();
                t_args.add("--scan-zip");
                t_args.add("--scan-log4j1");
                t_args.add("--scan-logback");
                for (String arg : cargs) {
                    if ( ! (
                            arg.equals("--scan-zip")
                                    || arg.equals("--scan-log4j1")
                                    || arg.equals("--scan-logback")
                    )) {
                        t_args.add(arg);
                    }
                }
                ret = t_args.toArray(new String[0]);
                break;
        }
        return ret;
    }

}
