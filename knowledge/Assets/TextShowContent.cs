using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class TextShowContent : MonoBehaviour, IDragHandler, IBeginDragHandler
{
    private RectTransform m_content, m_rect;
    public float m_mouseSensitivity; 
    private Vector3 m_moveOffset;

    // Start is called before the first frame update
    private void Awake()
    {
        m_rect = transform.GetComponent<RectTransform>();
        m_content = transform.Find("Content").GetComponent<RectTransform>();
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
        m_moveOffset = Input.mousePosition;
    }

    public void OnDrag(PointerEventData eventData)
    {
        float maxOffsetY = m_content.rect.height - m_rect.rect.height - m_content.offsetMax.y;
        float offsetY = Mathf.Min(maxOffsetY, (Input.mousePosition.y - m_moveOffset.y) * m_mouseSensitivity);
        offsetY = Mathf.Max(-m_content.offsetMax.y, offsetY);
        Vector2 newOffsetMin = m_content.offsetMin;
        Vector2 newOffsetMax = m_content.offsetMax;
        newOffsetMin.y += offsetY;
        newOffsetMax.y += offsetY;
        m_content.offsetMin = newOffsetMin;
        m_content.offsetMax = newOffsetMax;
    }

    // Update is called once per frame
    void Update()
    {
        print(m_content.offsetMin);
        print(m_content.offsetMax);
    }

}
