using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RecordManager : MonoBehaviour
{
    public GameObject m_RecordScanView;
    public GameObject m_RecordAdditionView;
    private GameObject m_currentView;
    private Dictionary<string, GameObject> m_ViewMapping;

    private void Awake()
    {
        m_currentView = m_RecordScanView;
        m_ViewMapping = new Dictionary<string, GameObject>
        {
            { "RecordScanView", m_RecordScanView },
            { "RecordAdditionView", m_RecordAdditionView}
        };
    }

    // Update is called once per frame
    private void Update()
    {
        
    }

    public void GoToView(string viewName)
    {
        m_currentView.SetActive(false);
        m_currentView = m_ViewMapping[viewName];
        m_currentView.SetActive(true);
    }

    public void GoToRecordScanView()
    {
        GoToView("RecordScanView");
    }

    public void GoToRecordAdditionView()
    {
        GoToView("RecordAdditionView");
    }
}
