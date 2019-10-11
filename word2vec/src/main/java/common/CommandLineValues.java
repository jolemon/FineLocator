package common;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

public class CommandLineValues {

    @Option(name = "-source", required = true)
    public String source_dir ;

    @Option(name = "-target")
    public String target_dir ;

    @Option(name = "--fit")
    public int fit = 0;

    @Option(name = "--num_threads")
    public int NumThreads = 32;


    public CommandLineValues(String... args) throws CmdLineException {
        CmdLineParser parser = new CmdLineParser(this);
        try {
            parser.parseArgument(args);
        } catch (CmdLineException e) {
            System.err.println(e.getMessage());
            parser.printUsage(System.err);
            throw e;
        }
    }

    public CommandLineValues(){}
}
