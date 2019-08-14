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
    public List<RecordInfo> RecordList { get; set; }
    public RecordDataStorage()
    {
        RecordList = new List<RecordInfo>();
    }
    public RecordDataStorage(List<RecordInfo> _recordList)
    {
        RecordList = _recordList;
    }
}

public enum ReviewingStatus
{
    Remember = 0,
    Forget,
    Skip,
}
