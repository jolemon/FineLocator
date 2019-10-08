package org.gajnineteen;

import java.nio.file.Path;
import java.util.concurrent.Callable;

public class BRTask implements Callable<Void> {

    Path filePath;

    public BRTask(Path filePath){
        this.filePath = filePath ;
    }

    @Override
    public Void call() throws Exception {
        return null;
    }
}
