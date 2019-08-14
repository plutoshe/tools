using System.Collections;
using UnityEngine;
using System.Collections.Generic;
using System;

public class RecordInfo
{
    public int ID { get; set; }
    public string Front { get; set; }
    public string Back { get; set; }
    public DateTime CreateDate { get; set; }
    public DateTime ReviewDate { get; set; }
    public DateTime ReviewDegree { get; set; }
    public List<string> Tags { get; set; }
}

public class RecordDataStorage
{
    public Dictionary<int, RecordInfo> RecordDict { get; set; }
    public int RecordIDNum { get; set; }

    public RecordDataStorage()
    {
        RecordDict = new Dictionary<int, RecordInfo>();
    }

    public RecordDataStorage(Dictionary<int, RecordInfo> _recordList)
    {
        RecordDict = _recordList;
    }

    public void CombineDerivedeReviewingIndexing(ReviewingIndexing ri)
    {
        for (int i = 0; i < ri.RecordList.Count; i++)
        {
            if (ri.RecordList[i].ID >= RecordIDNum)
            {
                RecordDict.Add(ri.RecordList[i].ID, ri.RecordList[i]);
            }
            else
            {
                RecordDict[ri.RecordList[i].ID] = ri.RecordList[i];
            }
        }
        RecordIDNum = ri.RecordIDNum;
    }
}

public class ReviewingIndexing
{
    public List<RecordInfo> RecordList { get; set; }
    public int RecordIDNum { get; set; }
    public void AddRecord(RecordInfo record)
    {
        record.ID = RecordIDNum;
        RecordIDNum++;
        RecordList.Add(record);
    }
    public ReviewingIndexing()
    {
        RecordList = new List<RecordInfo>();
    }
}

public enum ReviewingStatus
{
    Remember = 0,
    Forget,
    Skip,
}
