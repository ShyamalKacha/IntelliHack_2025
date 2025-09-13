// API Documentation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add copy functionality to code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        // Create copy button
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        
        // Insert button before the code block
        block.parentNode.style.position = 'relative';
        block.parentNode.insertBefore(button, block);
        
        // Add click event to copy code
        button.addEventListener('click', function() {
            const text = block.textContent;
            navigator.clipboard.writeText(text).then(() => {
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        });
    });
    
    // Add anchor links to headings
    const headings = document.querySelectorAll('.endpoint h3');
    
    headings.forEach(heading => {
        const anchor = document.createElement('a');
        anchor.className = 'anchor-link';
        anchor.href = '#' + heading.id;
        anchor.innerHTML = '🔗';
        heading.appendChild(anchor);
    });
});