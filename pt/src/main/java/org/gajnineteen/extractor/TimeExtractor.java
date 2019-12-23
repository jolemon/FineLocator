package org.gajnineteen.extractor;

import org.eclipse.jgit.api.BlameCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.blame.BlameResult;
import org.eclipse.jgit.diff.RawText;
import org.eclipse.jgit.internal.storage.file.FileRepository;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.PersonIdent;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;

import java.io.IOException;
import java.util.Date;

public class TimeExtractor {

    Repository repo ;
    Git git ;
    String filePath ;
    String commitID ;

    public TimeExtractor(String gitPathStr, String relativeFilePath, String commitID)  {
        try {
            this.repo = new FileRepository(gitPathStr) ;
        } catch (IOException e) {
            e.printStackTrace();
        }
        this.commitID = commitID;
        this.git = new Git(this.repo) ;
        this.filePath = relativeFilePath ;
    }

    // extract last modify time of method
    public Date extract(int startLineNum, int endLineNum) throws IOException, GitAPIException {

        Date latestDate = null ;
        BlameCommand blameCommand = git.blame() ;
        blameCommand.setFilePath(filePath) ;
        ObjectId commitID = repo.resolve(this.commitID) ;
        blameCommand.setStartCommit(commitID) ;
        BlameResult blameResult = blameCommand.call();
        RawText rawText = blameResult.getResultContents();
        for (int i=startLineNum ; i <= endLineNum ; i++) {
            RevCommit revCommit = blameResult.getSourceCommit(i) ;
            PersonIdent personIdent = revCommit.getAuthorIdent() ;
            Date date = personIdent.getWhen() ;
            if (latestDate == null) {
                latestDate = date ;
            } else if (date.after(latestDate)) {
                latestDate = date ;
            }
        }

        return latestDate;
    }

//    public static void main(String[] args) {
//        try {
//            Date date = new TimeExtractor("/Users/lienming/Downloads/bugcode/Lang_1/.git",
//            "src/main/java/org/apache/commons/lang3/AnnotationUtils.java", "2c454a4ce3fe771098746879b166ede2284b94f4" )
//                    .extract(0, 370) ;
//            System.out.println(date);
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }
}
