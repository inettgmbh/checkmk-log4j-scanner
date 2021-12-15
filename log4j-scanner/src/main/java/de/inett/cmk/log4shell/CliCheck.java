package de.inett.cmk.log4shell;

import com.logpresso.scanner.Log4j2Scanner;

public class CliCheck {
    public static void main(String[] args) {
        String[] n_args;
        switch (args.length) {
            case 0:
                n_args = new String[]{"/"};
                break;
            case 1:
                n_args = new String[]{args[0]};
                break;
            default:
                n_args = args;
                break;
        }
        System.out.println("<<<log4j_scanner>>>");
        Log4j2Scanner.main(n_args);
    }
}
