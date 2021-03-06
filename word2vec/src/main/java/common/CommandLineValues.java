package common;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

public class CommandLineValues {

    @Option(name = "-name", required = true)
    public String model_name ;

    @Option(name = "-source", required = true)
    public String source_dir ;

    @Option(name = "-target")
    public String target_dir ;

    @Option(name = "-tfidf")
    public String tfidf_dir ;

    @Option(name = "-correspond")
    public String correspond_dir ;

    @Option(name = "-type", required = true)
    public String type ;

    @Option(name = "-fit")
    public int fit = 0 ;

    @Option(name = "-dim", required = true)
    public int dim;

    @Option(name = "-epochs")
    public int epochs = 10 ;

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
