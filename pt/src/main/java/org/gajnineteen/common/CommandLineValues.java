package org.gajnineteen.common;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

public class CommandLineValues {

    // Notice: source_dir should be directory, not a file, because later we will replace this name with none in TimeExtractor
    @Option(name = "-source")
    public String source_dir ;

    @Option(name = "-target")
    public String target_dir ;

    @Option(name = "-correspond")
    public String correspond_dir ;

    @Option(name = "-git")
    public String git_dir ;

    @Option(name = "-type")
    public String type ;

    @Option(name = "-commitID")
    public String commitID ;

    @Option(name = "--num_threads")
    public int NumThreads = 16;


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
