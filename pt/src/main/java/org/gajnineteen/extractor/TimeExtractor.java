package org.gajnineteen.extractor;

import org.eclipse.jgit.api.BlameCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.blame.BlameResult;
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

    public TimeExtractor(String gitPathStr, String relativeFilePath)  {
        try {
            this.repo = new FileRepository(gitPathStr) ;
        } catch (IOException e) {
            e.printStackTrace();
        }
        this.git = new Git(this.repo) ;
        this.filePath = relativeFilePath ;
    }

    // extract last modify time of method
    public Date extract(int startLineNum, int endLineNum) throws IOException, GitAPIException {

        Date latestDate = null ;
        BlameCommand blameCommand = git.blame() ;
        blameCommand.setFilePath(filePath) ;
        ObjectId commitID = repo.resolve("HEAD~~") ;
        blameCommand.setStartCommit(commitID) ;
        BlameResult blameResult = null;
        blameResult = blameCommand.call();

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
//            Date date = new TimeExtractor("/Users/lienming/Downloads/bugcode/Time_3/.git", "src/main/java/org/joda/time/format/PeriodFormatterBuilder.java")
//                    .extract(101, 103) ;
//            System.out.println(date);
//        } catch (IOException e) {
//            e.printStackTrace();
//        } catch (GitAPIException e) {
//            e.printStackTrace();
//        }
//    }
}
