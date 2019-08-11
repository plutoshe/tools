using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TextShowContent : MonoBehaviour
{
    private RectTransform m_content;
    // Start is called before the first frame update
    private void Awake()
    {


        
    }
    private void Start()
    {
        m_content = transform.Find("Content").GetComponent<RectTransform>();
        //print(m_content.rect.yMax);
        //print(m_content.rect.yMin);
        //print(transform.GetComponent<RectTransform>().rect.height);
        //print(transform.Find("Content").GetComponent<RectTransform>().rect.height);
        //print(m_content.rect.height);
    }

    // Update is called once per frame
    void Update()
    {
        float offsetY = m_content.rect.height -
            transform.GetComponent<RectTransform>().rect.height;

        print(offsetY);
        if (m_content.offsetMax.y == 0)
        {
            Vector2 newOffsetMin = m_content.offsetMin;
            Vector2 newOffsetMax = m_content.offsetMax;
            newOffsetMin.y += offsetY;
            newOffsetMax.y += offsetY;
            m_content.offsetMin = newOffsetMin;
            m_content.offsetMax = newOffsetMax;
        }
        //m_content.localPosition = newPosition;
    }

}
