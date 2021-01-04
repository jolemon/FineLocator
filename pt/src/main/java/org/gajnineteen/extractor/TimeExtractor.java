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

import java.util.Date;

public class TimeExtractor {
//    private static volatile TimeExtractor timeExtractor;
    private static TimeExtractor timeExtractor;
    private Repository repository;
    private final Git git;
    private ObjectId commitId;

    private TimeExtractor(String gitPathStr, String commitID)  {
        try {
            repository = new FileRepository(gitPathStr) ;
            commitId = repository.resolve(commitID);
        } catch (Exception e) {
            e.printStackTrace();
        }
        git = new Git(repository);
    }

    public static TimeExtractor getInstance(String gitPathStr, String commitID) {
        if (null == timeExtractor) {
//            synchronized (TimeExtractor.class) {
//                if (null == timeExtractor) {
//                    timeExtractor = new TimeExtractor(gitPathStr, commitID);
//                }
//            }
            timeExtractor = new TimeExtractor(gitPathStr, commitID);
        }
        return timeExtractor;
    }

    // filePath 是".git"目录的相对路径，比如".git"目录是${proj}/.git，文件是${proj}/a/b.java， 则relativeFilePath是a/b.java
    public Date extract(String filePath, int startLineNum, int endLineNum) throws GitAPIException {
        Date latestDate = null ;
        BlameCommand blameCommand = git.blame() ;
        blameCommand.setFilePath(filePath) ;
        blameCommand.setStartCommit(this.commitId);
        BlameResult blameResult = blameCommand.call();
        if (blameResult == null) {
            System.out.println("time null - " + filePath + "是相对路径吗?");
            return null;
        }
//        RawText rawText = blameResult.getResultContents();
//        System.out.println(rawText.size());
        for (int i=startLineNum; i<=endLineNum; i++) {
            RevCommit revCommit;
            try {
                revCommit = blameResult.getSourceCommit(i-1) ;  // idx - line to read data of, 0 based.
            } catch (ArrayIndexOutOfBoundsException e) {
                // 处理开始/结束行数计算错误的异常情况
                System.out.println(filePath + " 行数非法:" + i);
                break;
            }
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

}
