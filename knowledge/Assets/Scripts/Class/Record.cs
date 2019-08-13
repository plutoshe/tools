using System.Collections;
using UnityEngine;
using System.Collections.Generic;

public class RecordInfo
{
    public int ID { get; set; }
    public string Front { get; set; }
    public string Back { get; set; }
}

public class RecordDataStorage
{
    public List<RecordInfo> RecordList { get; set; }
}
